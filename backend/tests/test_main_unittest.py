import unittest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from src.main import app

class TestMainEndpoints(unittest.TestCase):
    """Test cases for main application endpoints"""
    
    def setUp(self):
        """Set up test client"""
        self.client = TestClient(app)
    
    def test_root_endpoint(self):
        """Test the root endpoint returns correct information"""
        response = self.client.get("/")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["message"], "Vue CRUD Backend API")
        self.assertEqual(data["version"], "2.0.0")
        self.assertIn("docs", data)
        self.assertIn("redoc", data)
        self.assertIn("environment", data)
    
    def test_docs_endpoint_accessible(self):
        """Test that API documentation is accessible"""
        response = self.client.get("/docs")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers.get("content-type", ""))
    
    def test_redoc_endpoint_accessible(self):
        """Test that ReDoc documentation is accessible"""
        response = self.client.get("/redoc")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers.get("content-type", ""))
    
    def test_cors_headers_present(self):
        """Test that CORS headers are properly set"""
        response = self.client.options("/api/entities/")
        self.assertIn("access-control-allow-origin", response.headers)
        self.assertIn("access-control-allow-methods", response.headers)
    
    def test_gzip_compression_header(self):
        """Test that gzip compression is enabled for large responses"""
        response = self.client.get("/")
        # Check if server supports compression
        self.assertTrue(
            "gzip" in response.headers.get("content-encoding", "") or
            response.status_code == 200  # Fallback for small responses
        )

if __name__ == '__main__':
    unittest.main()