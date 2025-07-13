import unittest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient
from src.main import app
from src.models.entity import Entity, EntityCreate, EntityUpdate
from datetime import datetime

class TestEntityEndpoints(unittest.TestCase):
    """Test cases for entity CRUD endpoints"""
    
    def setUp(self):
        """Set up test client and sample data"""
        self.client = TestClient(app)
        self.sample_entity = {
            "name": "Test Entity",
            "entity_type": "skill",
            "entity_parent": None,
            "color": "#ff0000",
            "icon": "test-icon"
        }
        self.sample_entity_response = {
            "id": 1,
            "name": "Test Entity",
            "entity_type": "skill",
            "entity_parent": None,
            "color": "#ff0000",
            "icon": "test-icon",
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
    
    @patch('src.services.entity_service.entity_service.create')
    def test_create_entity_success(self, mock_create):
        """Test successful entity creation"""
        # Mock service response
        mock_entity = Entity(**self.sample_entity_response)
        mock_create.return_value = mock_entity
        
        response = self.client.post("/api/entities/", json=self.sample_entity)
        
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["name"], self.sample_entity["name"])
        self.assertEqual(data["entity_type"], self.sample_entity["entity_type"])
        self.assertIn("id", data)
        mock_create.assert_called_once()
    
    @patch('src.services.entity_service.entity_service.create')
    def test_create_entity_service_error(self, mock_create):
        """Test entity creation when service raises exception"""
        mock_create.side_effect = Exception("Database error")
        
        response = self.client.post("/api/entities/", json=self.sample_entity)
        
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("Failed to create entity", data["detail"])
    
    def test_create_entity_invalid_type(self):
        """Test entity creation with invalid entity type"""
        invalid_entity = {
            **self.sample_entity,
            "entity_type": "invalid_type"
        }
        
        response = self.client.post("/api/entities/", json=invalid_entity)
        
        self.assertEqual(response.status_code, 422)
        data = response.json()
        self.assertIn("detail", data)
    
    def test_create_entity_missing_name(self):
        """Test entity creation with missing required name field"""
        invalid_entity = {
            "entity_type": "skill",
            "color": "#ff0000"
        }
        
        response = self.client.post("/api/entities/", json=invalid_entity)
        
        self.assertEqual(response.status_code, 422)
    
    @patch('src.services.entity_service.entity_service.get_all')
    def test_get_all_entities_success(self, mock_get_all):
        """Test successful retrieval of all entities"""
        mock_entities = [Entity(**self.sample_entity_response)]
        mock_get_all.return_value = mock_entities
        
        response = self.client.get("/api/entities/")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], self.sample_entity["name"])
        mock_get_all.assert_called_once()
    
    @patch('src.services.entity_service.entity_service.get_all')
    def test_get_all_entities_empty(self, mock_get_all):
        """Test retrieval when no entities exist"""
        mock_get_all.return_value = []
        
        response = self.client.get("/api/entities/")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)
    
    @patch('src.services.entity_service.entity_service.get_by_id')
    def test_get_entity_by_id_success(self, mock_get_by_id):
        """Test successful retrieval of entity by ID"""
        mock_entity = Entity(**self.sample_entity_response)
        mock_get_by_id.return_value = mock_entity
        
        response = self.client.get("/api/entities/1")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["name"], self.sample_entity["name"])
        mock_get_by_id.assert_called_once_with(1)
    
    @patch('src.services.entity_service.entity_service.get_by_id')
    def test_get_entity_by_id_not_found(self, mock_get_by_id):
        """Test retrieval of non-existent entity"""
        mock_get_by_id.return_value = None
        
        response = self.client.get("/api/entities/999")
        
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data["detail"], "Entity not found")
    
    @patch('src.services.entity_service.entity_service.update')
    def test_update_entity_success(self, mock_update):
        """Test successful entity update"""
        updated_entity_data = {
            **self.sample_entity_response,
            "name": "Updated Entity Name"
        }
        mock_entity = Entity(**updated_entity_data)
        mock_update.return_value = mock_entity
        
        update_data = {"name": "Updated Entity Name"}
        response = self.client.put("/api/entities/1", json=update_data)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Updated Entity Name")
        self.assertEqual(data["id"], 1)
        mock_update.assert_called_once()
    
    @patch('src.services.entity_service.entity_service.update')
    def test_update_entity_not_found(self, mock_update):
        """Test update of non-existent entity"""
        mock_update.return_value = None
        
        update_data = {"name": "Updated Entity Name"}
        response = self.client.put("/api/entities/999", json=update_data)
        
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data["detail"], "Entity not found")
    
    @patch('src.services.entity_service.entity_service.delete')
    def test_delete_entity_success(self, mock_delete):
        """Test successful entity deletion"""
        mock_delete.return_value = True
        
        response = self.client.delete("/api/entities/1")
        
        self.assertEqual(response.status_code, 204)
        mock_delete.assert_called_once_with(1)
    
    @patch('src.services.entity_service.entity_service.delete')
    def test_delete_entity_not_found(self, mock_delete):
        """Test deletion of non-existent entity"""
        mock_delete.return_value = False
        
        response = self.client.delete("/api/entities/999")
        
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data["detail"], "Entity not found")

if __name__ == '__main__':
    unittest.main()