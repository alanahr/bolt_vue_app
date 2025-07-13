import unittest
from unittest.mock import patch, AsyncMock, MagicMock
from src.services.entity_service import EntityService
from src.services.position_service import PositionService
from src.models.entity import EntityCreate, EntityUpdate
from src.models.position import PositionCreate, PositionUpdate
from datetime import datetime
import asyncio

class TestEntityService(unittest.TestCase):
    """Test cases for EntityService"""
    
    def setUp(self):
        """Set up test service and sample data"""
        self.service = EntityService()
        self.sample_entity_data = {
            "name": "Test Entity",
            "entity_type": "skill",
            "entity_parent": None,
            "color": "#ff0000",
            "icon": "test-icon"
        }
        self.sample_db_entity = {
            "_id": "507f1f77bcf86cd799439011",
            "id": 1,
            **self.sample_entity_data,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
    
    @patch('src.config.database.database.get_db')
    def test_get_next_id_first_entity(self, mock_get_db):
        """Test getting next ID when no entities exist"""
        mock_db = MagicMock()
        mock_collection = AsyncMock()
        mock_collection.find_one = AsyncMock(return_value=None)
        mock_db.__getitem__.return_value = mock_collection
        mock_get_db.return_value = mock_db
        
        async def run_test():
            next_id = await self.service.get_next_id()
            self.assertEqual(next_id, 1)
        
        asyncio.run(run_test())
    
    @patch('src.config.database.database.get_db')
    def test_get_next_id_existing_entities(self, mock_get_db):
        """Test getting next ID when entities exist"""
        mock_db = MagicMock()
        mock_collection = AsyncMock()
        mock_collection.find_one = AsyncMock(return_value={"id": 5})
        mock_db.__getitem__.return_value = mock_collection
        mock_get_db.return_value = mock_db
        
        async def run_test():
            next_id = await self.service.get_next_id()
            self.assertEqual(next_id, 6)
        
        asyncio.run(run_test())
    
    @patch('src.config.database.database.get_db')
    def test_create_entity_success(self, mock_get_db):
        """Test successful entity creation"""
        mock_db = MagicMock()
        mock_collection = AsyncMock()
        
        # Mock get_next_id
        mock_collection.find_one = AsyncMock(return_value=None)
        
        # Mock insert_one
        mock_result = MagicMock()
        mock_result.inserted_id = "507f1f77bcf86cd799439011"
        mock_collection.insert_one = AsyncMock(return_value=mock_result)
        
        mock_db.__getitem__.return_value = mock_collection
        mock_get_db.return_value = mock_db
        
        async def run_test():
            entity_create = EntityCreate(**self.sample_entity_data)
            result = await self.service.create(entity_create)
            
            self.assertEqual(result.name, self.sample_entity_data["name"])
            self.assertEqual(result.entity_type, self.sample_entity_data["entity_type"])
            self.assertEqual(result.id, 1)
            self.assertIsInstance(result.created_at, datetime)
            self.assertIsInstance(result.updated_at, datetime)
        
        asyncio.run(run_test())
    
    @patch('src.config.database.database.get_db')
    def test_get_all_entities(self, mock_get_db):
        """Test retrieving all entities"""
        mock_db = MagicMock()
        mock_collection = AsyncMock()
        
        # Mock cursor and async iteration
        mock_cursor = AsyncMock()
        mock_cursor.__aiter__ = AsyncMock(return_value=iter([self.sample_db_entity]))
        mock_collection.find.return_value = mock_cursor
        
        mock_db.__getitem__.return_value = mock_collection
        mock_get_db.return_value = mock_db
        
        async def run_test():
            entities = await self.service.get_all()
            
            self.assertEqual(len(entities), 1)
            self.assertEqual(entities[0].name, self.sample_entity_data["name"])
            self.assertEqual(entities[0].id, 1)
        
        asyncio.run(run_test())
    
    @patch('src.config.database.database.get_db')
    def test_get_by_id_found(self, mock_get_db):
        """Test retrieving entity by ID when found"""
        mock_db = MagicMock()
        mock_collection = AsyncMock()
        mock_collection.find_one = AsyncMock(return_value=self.sample_db_entity)
        mock_db.__getitem__.return_value = mock_collection
        mock_get_db.return_value = mock_db
        
        async def run_test():
            entity = await self.service.get_by_id(1)
            
            self.assertIsNotNone(entity)
            self.assertEqual(entity.name, self.sample_entity_data["name"])
            self.assertEqual(entity.id, 1)
        
        asyncio.run(run_test())
    
    @patch('src.config.database.database.get_db')
    def test_get_by_id_not_found(self, mock_get_db):
        """Test retrieving entity by ID when not found"""
        mock_db = MagicMock()
        mock_collection = AsyncMock()
        mock_collection.find_one = AsyncMock(return_value=None)
        mock_db.__getitem__.return_value = mock_collection
        mock_get_db.return_value = mock_db
        
        async def run_test():
            entity = await self.service.get_by_id(999)
            self.assertIsNone(entity)
        
        asyncio.run(run_test())
    
    @patch('src.config.database.database.get_db')
    def test_update_entity_success(self, mock_get_db):
        """Test successful entity update"""
        mock_db = MagicMock()
        mock_collection = AsyncMock()
        
        updated_entity = {
            **self.sample_db_entity,
            "name": "Updated Entity Name"
        }
        mock_collection.find_one_and_update = AsyncMock(return_value=updated_entity)
        mock_db.__getitem__.return_value = mock_collection
        mock_get_db.return_value = mock_db
        
        async def run_test():
            entity_update = EntityUpdate(name="Updated Entity Name")
            result = await self.service.update(1, entity_update)
            
            self.assertIsNotNone(result)
            self.assertEqual(result.name, "Updated Entity Name")
            self.assertEqual(result.id, 1)
        
        asyncio.run(run_test())
    
    @patch('src.config.database.database.get_db')
    def test_delete_entity_success(self, mock_get_db):
        """Test successful entity deletion"""
        mock_db = MagicMock()
        mock_collection = AsyncMock()
        
        mock_result = MagicMock()
        mock_result.deleted_count = 1
        mock_collection.delete_one = AsyncMock(return_value=mock_result)
        mock_db.__getitem__.return_value = mock_collection
        mock_get_db.return_value = mock_db
        
        async def run_test():
            result = await self.service.delete(1)
            self.assertTrue(result)
        
        asyncio.run(run_test())
    
    @patch('src.config.database.database.get_db')
    def test_delete_entity_not_found(self, mock_get_db):
        """Test entity deletion when entity not found"""
        mock_db = MagicMock()
        mock_collection = AsyncMock()
        
        mock_result = MagicMock()
        mock_result.deleted_count = 0
        mock_collection.delete_one = AsyncMock(return_value=mock_result)
        mock_db.__getitem__.return_value = mock_collection
        mock_get_db.return_value = mock_db
        
        async def run_test():
            result = await self.service.delete(999)
            self.assertFalse(result)
        
        asyncio.run(run_test())


class TestPositionService(unittest.TestCase):
    """Test cases for PositionService"""
    
    def setUp(self):
        """Set up test service and sample data"""
        self.service = PositionService()
        self.sample_position_data = {
            "name": "Test Position",
            "start_year": 2023,
            "start_month": 1,
            "start_day": 15,
            "salary": 75000.0,
            "details": []
        }
        self.sample_db_position = {
            "_id": "507f1f77bcf86cd799439011",
            "id": 1,
            **self.sample_position_data,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
    
    @patch('src.config.database.database.get_db')
    def test_create_position_success(self, mock_get_db):
        """Test successful position creation"""
        mock_db = MagicMock()
        mock_collection = AsyncMock()
        
        # Mock get_next_id
        mock_collection.find_one = AsyncMock(return_value=None)
        
        # Mock insert_one
        mock_result = MagicMock()
        mock_result.inserted_id = "507f1f77bcf86cd799439011"
        mock_collection.insert_one = AsyncMock(return_value=mock_result)
        
        mock_db.__getitem__.return_value = mock_collection
        mock_get_db.return_value = mock_db
        
        async def run_test():
            position_create = PositionCreate(**self.sample_position_data)
            result = await self.service.create(position_create)
            
            self.assertEqual(result.name, self.sample_position_data["name"])
            self.assertEqual(result.start_year, self.sample_position_data["start_year"])
            self.assertEqual(result.salary, self.sample_position_data["salary"])
            self.assertEqual(result.id, 1)
            self.assertIsInstance(result.created_at, datetime)
        
        asyncio.run(run_test())
    
    @patch('src.config.database.database.get_db')
    def test_get_all_positions(self, mock_get_db):
        """Test retrieving all positions"""
        mock_db = MagicMock()
        mock_collection = AsyncMock()
        
        # Mock cursor and async iteration
        mock_cursor = AsyncMock()
        mock_cursor.__aiter__ = AsyncMock(return_value=iter([self.sample_db_position]))
        mock_collection.find.return_value = mock_cursor
        
        mock_db.__getitem__.return_value = mock_collection
        mock_get_db.return_value = mock_db
        
        async def run_test():
            positions = await self.service.get_all()
            
            self.assertEqual(len(positions), 1)
            self.assertEqual(positions[0].name, self.sample_position_data["name"])
            self.assertEqual(positions[0].id, 1)
        
        asyncio.run(run_test())
    
    @patch('src.config.database.database.get_db')
    def test_update_position_partial(self, mock_get_db):
        """Test partial position update"""
        mock_db = MagicMock()
        mock_collection = AsyncMock()
        
        updated_position = {
            **self.sample_db_position,
            "salary": 85000.0
        }
        mock_collection.find_one_and_update = AsyncMock(return_value=updated_position)
        mock_db.__getitem__.return_value = mock_collection
        mock_get_db.return_value = mock_db
        
        async def run_test():
            position_update = PositionUpdate(salary=85000.0)
            result = await self.service.update(1, position_update)
            
            self.assertIsNotNone(result)
            self.assertEqual(result.salary, 85000.0)
            self.assertEqual(result.name, self.sample_position_data["name"])  # Unchanged
        
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()