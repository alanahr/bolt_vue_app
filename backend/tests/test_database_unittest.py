import unittest
from unittest.mock import patch, AsyncMock, MagicMock
from src.config.database import Database
import asyncio

class TestDatabase(unittest.TestCase):
    """Test cases for Database configuration and connection"""
    
    def setUp(self):
        """Set up test database instance"""
        self.database = Database()
    
    def test_database_initialization(self):
        """Test database instance initialization"""
        self.assertIsNone(self.database.client)
        self.assertIsNone(self.database.db)
        self.assertFalse(self.database.is_connected)
    
    def test_is_ready_false_when_not_connected(self):
        """Test is_ready returns False when not connected"""
        self.assertFalse(self.database.is_ready())
    
    def test_get_db_raises_error_when_not_connected(self):
        """Test get_db raises error when not connected"""
        with self.assertRaises(ConnectionError) as context:
            self.database.get_db()
        
        self.assertIn("Database not connected", str(context.exception))
    
    @patch('src.config.database.AsyncIOMotorClient')
    def test_connect_success(self, mock_client_class):
        """Test successful database connection"""
        # Mock the client and its methods
        mock_client = AsyncMock()
        mock_client.admin.command = AsyncMock(return_value={"ok": 1})
        mock_client_class.return_value = mock_client
        
        # Mock database
        mock_db = MagicMock()
        mock_client.__getitem__.return_value = mock_db
        
        async def run_test():
            result = await self.database.connect()
            
            self.assertTrue(self.database.is_connected)
            self.assertIsNotNone(self.database.client)
            self.assertIsNotNone(self.database.db)
            self.assertEqual(result, mock_db)
            
            # Verify client was created with correct parameters
            mock_client_class.assert_called_once()
            call_args = mock_client_class.call_args
            self.assertIn("maxPoolSize", call_args[1])
            self.assertEqual(call_args[1]["maxPoolSize"], 10)
        
        asyncio.run(run_test())
    
    @patch('src.config.database.AsyncIOMotorClient')
    def test_connect_failure(self, mock_client_class):
        """Test database connection failure"""
        # Mock client to raise exception on ping
        mock_client = AsyncMock()
        mock_client.admin.command = AsyncMock(side_effect=Exception("Connection failed"))
        mock_client_class.return_value = mock_client
        
        async def run_test():
            with self.assertRaises(Exception) as context:
                await self.database.connect()
            
            self.assertIn("Connection failed", str(context.exception))
            self.assertFalse(self.database.is_connected)
        
        asyncio.run(run_test())
    
    @patch.dict('os.environ', {
        'MONGODB_URI': 'mongodb://test:test@localhost:27017/test_db?authSource=admin',
        'MONGODB_DB_NAME': 'test_database'
    })
    @patch('src.config.database.AsyncIOMotorClient')
    def test_connect_with_environment_variables(self, mock_client_class):
        """Test connection uses environment variables"""
        mock_client = AsyncMock()
        mock_client.admin.command = AsyncMock(return_value={"ok": 1})
        mock_client_class.return_value = mock_client
        
        async def run_test():
            await self.database.connect()
            
            # Verify client was created with environment URI
            mock_client_class.assert_called_once()
            call_args = mock_client_class.call_args
            self.assertEqual(
                call_args[0][0], 
                'mongodb://test:test@localhost:27017/test_db?authSource=admin'
            )
        
        asyncio.run(run_test())
    
    def test_disconnect_when_not_connected(self):
        """Test disconnect when not connected"""
        async def run_test():
            # Should not raise exception
            await self.database.disconnect()
            self.assertFalse(self.database.is_connected)
        
        asyncio.run(run_test())
    
    def test_disconnect_success(self):
        """Test successful disconnect"""
        # Set up connected state
        mock_client = AsyncMock()
        self.database.client = mock_client
        self.database.is_connected = True
        
        async def run_test():
            await self.database.disconnect()
            
            mock_client.close.assert_called_once()
            self.assertFalse(self.database.is_connected)
        
        asyncio.run(run_test())
    
    def test_disconnect_with_error(self):
        """Test disconnect when close raises exception"""
        mock_client = AsyncMock()
        mock_client.close = AsyncMock(side_effect=Exception("Close failed"))
        self.database.client = mock_client
        self.database.is_connected = True
        
        async def run_test():
            with self.assertRaises(Exception) as context:
                await self.database.disconnect()
            
            self.assertIn("Close failed", str(context.exception))
        
        asyncio.run(run_test())
    
    def test_is_ready_true_when_connected(self):
        """Test is_ready returns True when properly connected"""
        # Simulate connected state
        self.database.is_connected = True
        self.database.db = MagicMock()
        
        self.assertTrue(self.database.is_ready())
    
    def test_get_db_success_when_connected(self):
        """Test get_db returns database when connected"""
        mock_db = MagicMock()
        self.database.is_connected = True
        self.database.db = mock_db
        
        result = self.database.get_db()
        self.assertEqual(result, mock_db)

if __name__ == '__main__':
    unittest.main()