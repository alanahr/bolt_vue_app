import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import Request, HTTPException
from fastapi.testclient import TestClient
from src.middleware.rate_limit import RateLimitMiddleware
from src.main import app
import time

class TestRateLimitMiddleware(unittest.TestCase):
    """Test cases for RateLimitMiddleware"""
    
    def setUp(self):
        """Set up test middleware and mock app"""
        self.mock_app = MagicMock()
        self.middleware = RateLimitMiddleware(self.mock_app, calls=5, period=60)
    
    def test_middleware_initialization(self):
        """Test middleware initialization with default values"""
        middleware = RateLimitMiddleware(self.mock_app)
        self.assertEqual(middleware.calls, 100)  # Default from env or fallback
        self.assertIsInstance(middleware.clients, dict)
    
    def test_middleware_initialization_with_params(self):
        """Test middleware initialization with custom parameters"""
        middleware = RateLimitMiddleware(self.mock_app, calls=10, period=30)
        self.assertEqual(middleware.calls, 10)
        self.assertEqual(middleware.period, 30)
    
    @patch.dict('os.environ', {
        'RATE_LIMIT_MAX_REQUESTS': '50',
        'RATE_LIMIT_WINDOW_MS': '30000'
    })
    def test_middleware_uses_environment_variables(self):
        """Test middleware uses environment variables when available"""
        middleware = RateLimitMiddleware(self.mock_app)
        self.assertEqual(middleware.calls, 50)
        self.assertEqual(middleware.period, 30)  # 30000ms / 1000
    
    async def test_health_check_bypass(self):
        """Test that health check endpoints bypass rate limiting"""
        mock_request = MagicMock()
        mock_request.url.path = "/health"
        mock_request.client.host = "127.0.0.1"
        
        mock_call_next = AsyncMock()
        mock_response = MagicMock()
        mock_call_next.return_value = mock_response
        
        result = await self.middleware.dispatch(mock_request, mock_call_next)
        
        self.assertEqual(result, mock_response)
        mock_call_next.assert_called_once_with(mock_request)
        # Should not add any entries to clients dict
        self.assertEqual(len(self.middleware.clients), 0)
    
    async def test_first_request_allowed(self):
        """Test that first request from client is allowed"""
        mock_request = MagicMock()
        mock_request.url.path = "/api/entities"
        mock_request.client.host = "127.0.0.1"
        
        mock_call_next = AsyncMock()
        mock_response = MagicMock()
        mock_call_next.return_value = mock_response
        
        result = await self.middleware.dispatch(mock_request, mock_call_next)
        
        self.assertEqual(result, mock_response)
        mock_call_next.assert_called_once_with(mock_request)
        # Should add one entry for the client
        self.assertEqual(len(self.middleware.clients["127.0.0.1"]), 1)
    
    async def test_multiple_requests_within_limit(self):
        """Test multiple requests within rate limit are allowed"""
        mock_request = MagicMock()
        mock_request.url.path = "/api/entities"
        mock_request.client.host = "127.0.0.1"
        
        mock_call_next = AsyncMock()
        mock_response = MagicMock()
        mock_call_next.return_value = mock_response
        
        # Make multiple requests within limit
        for i in range(3):
            result = await self.middleware.dispatch(mock_request, mock_call_next)
            self.assertEqual(result, mock_response)
        
        # Should have 3 entries for the client
        self.assertEqual(len(self.middleware.clients["127.0.0.1"]), 3)
        self.assertEqual(mock_call_next.call_count, 3)
    
    async def test_rate_limit_exceeded(self):
        """Test that rate limit is enforced when exceeded"""
        mock_request = MagicMock()
        mock_request.url.path = "/api/entities"
        mock_request.client.host = "127.0.0.1"
        
        mock_call_next = AsyncMock()
        mock_response = MagicMock()
        mock_call_next.return_value = mock_response
        
        # Make requests up to the limit
        for i in range(5):
            await self.middleware.dispatch(mock_request, mock_call_next)
        
        # Next request should raise HTTPException
        with self.assertRaises(HTTPException) as context:
            await self.middleware.dispatch(mock_request, mock_call_next)
        
        self.assertEqual(context.exception.status_code, 429)
        self.assertIn("Too many requests", context.exception.detail)
    
    @patch('time.time')
    async def test_old_requests_cleaned_up(self, mock_time):
        """Test that old requests are cleaned up from the tracking"""
        mock_request = MagicMock()
        mock_request.url.path = "/api/entities"
        mock_request.client.host = "127.0.0.1"
        
        mock_call_next = AsyncMock()
        mock_response = MagicMock()
        mock_call_next.return_value = mock_response
        
        # Simulate time progression
        current_time = 1000.0
        mock_time.return_value = current_time
        
        # Make initial requests
        for i in range(3):
            await self.middleware.dispatch(mock_request, mock_call_next)
            current_time += 1
            mock_time.return_value = current_time
        
        # Advance time beyond the window period
        current_time += 70  # Beyond 60 second window
        mock_time.return_value = current_time
        
        # Make another request - old requests should be cleaned up
        await self.middleware.dispatch(mock_request, mock_call_next)
        
        # Should only have 1 recent request
        self.assertEqual(len(self.middleware.clients["127.0.0.1"]), 1)
    
    async def test_different_clients_tracked_separately(self):
        """Test that different client IPs are tracked separately"""
        mock_call_next = AsyncMock()
        mock_response = MagicMock()
        mock_call_next.return_value = mock_response
        
        # Client 1
        mock_request1 = MagicMock()
        mock_request1.url.path = "/api/entities"
        mock_request1.client.host = "127.0.0.1"
        
        # Client 2
        mock_request2 = MagicMock()
        mock_request2.url.path = "/api/entities"
        mock_request2.client.host = "192.168.1.1"
        
        # Make requests from both clients
        for i in range(3):
            await self.middleware.dispatch(mock_request1, mock_call_next)
            await self.middleware.dispatch(mock_request2, mock_call_next)
        
        # Both clients should have their own tracking
        self.assertEqual(len(self.middleware.clients["127.0.0.1"]), 3)
        self.assertEqual(len(self.middleware.clients["192.168.1.1"]), 3)
        self.assertEqual(mock_call_next.call_count, 6)


class TestMiddlewareIntegration(unittest.TestCase):
    """Integration tests for middleware with FastAPI app"""
    
    def setUp(self):
        """Set up test client"""
        self.client = TestClient(app)
    
    def test_rate_limiting_in_app(self):
        """Test rate limiting works in the actual app"""
        # Make multiple requests quickly
        responses = []
        for i in range(10):
            response = self.client.get("/api/entities/")
            responses.append(response)
        
        # At least some requests should succeed
        success_count = sum(1 for r in responses if r.status_code == 200)
        self.assertGreater(success_count, 0)
        
        # If rate limiting is working, some might be 429 (depending on configuration)
        # This test mainly ensures the middleware doesn't break the app
    
    def test_health_endpoint_not_rate_limited(self):
        """Test health endpoint bypasses rate limiting"""
        # Make many requests to health endpoint
        for i in range(20):
            response = self.client.get("/health")
            self.assertEqual(response.status_code, 200)
    
    def test_cors_headers_present(self):
        """Test CORS middleware is working"""
        response = self.client.options("/api/entities/")
        
        # Should have CORS headers
        self.assertIn("access-control-allow-origin", response.headers)
        self.assertIn("access-control-allow-methods", response.headers)

if __name__ == '__main__':
    unittest.main()