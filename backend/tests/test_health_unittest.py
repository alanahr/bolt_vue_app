import unittest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient
from src.main import app
from src.config.database import database

class TestHealthEndpoints(unittest.TestCase):
    """Test cases for health check endpoints"""
    
    def setUp(self):
        """Set up test client"""
        self.client = TestClient(app)
    
    @patch('src.config.database.database.is_ready')
    @patch('src.config.database.database.get_db')
    def test_health_check_healthy(self, mock_get_db, mock_is_ready):
        """Test health check when database is healthy"""
        # Mock database as ready
        mock_is_ready.return_value = True
        
        # Mock database ping
        mock_db = AsyncMock()
        mock_db.command = AsyncMock(return_value={"ok": 1})
        mock_get_db.return_value = mock_db
        
        response = self.client.get("/health")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("timestamp", data)
        self.assertIn("system", data)
        self.assertIn("database", data)
        
        # Check system info structure
        system_info = data["system"]
        self.assertIn("cpu_percent", system_info)
        self.assertIn("memory", system_info)
        self.assertIn("python_version", system_info)
        
        # Check memory info structure
        memory_info = system_info["memory"]
        self.assertIn("total", memory_info)
        self.assertIn("available", memory_info)
        self.assertIn("percent", memory_info)
    
    @patch('src.config.database.database.is_ready')
    def test_health_check_database_disconnected(self, mock_is_ready):
        """Test health check when database is disconnected"""
        # Mock database as not ready
        mock_is_ready.return_value = False
        
        response = self.client.get("/health")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["database"]["status"], "disconnected")
    
    @patch('src.config.database.database.is_ready')
    @patch('src.config.database.database.get_db')
    @patch('psutil.cpu_percent')
    def test_health_check_with_system_error(self, mock_cpu, mock_get_db, mock_is_ready):
        """Test health check when system monitoring fails"""
        # Mock database as ready
        mock_is_ready.return_value = True
        mock_db = AsyncMock()
        mock_get_db.return_value = mock_db
        
        # Mock CPU monitoring to raise exception
        mock_cpu.side_effect = Exception("System monitoring error")
        
        response = self.client.get("/health")
        
        # Should still return 500 due to system error
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("error", data["detail"])

if __name__ == '__main__':
    unittest.main()