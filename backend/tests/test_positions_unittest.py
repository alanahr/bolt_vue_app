import unittest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient
from src.main import app
from src.models.position import Position, PositionCreate, PositionUpdate
from datetime import datetime

class TestPositionEndpoints(unittest.TestCase):
    """Test cases for position CRUD endpoints"""
    
    def setUp(self):
        """Set up test client and sample data"""
        self.client = TestClient(app)
        self.sample_position = {
            "name": "Test Position",
            "start_year": 2023,
            "start_month": 1,
            "start_day": 15,
            "end_year": None,
            "end_month": None,
            "end_day": None,
            "salary": 75000.0,
            "details": []
        }
        self.sample_position_response = {
            "id": 1,
            "name": "Test Position",
            "start_year": 2023,
            "start_month": 1,
            "start_day": 15,
            "end_year": None,
            "end_month": None,
            "end_day": None,
            "salary": 75000.0,
            "details": [],
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
    
    @patch('src.services.position_service.position_service.create')
    def test_create_position_success(self, mock_create):
        """Test successful position creation"""
        mock_position = Position(**self.sample_position_response)
        mock_create.return_value = mock_position
        
        response = self.client.post("/api/positions/", json=self.sample_position)
        
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["name"], self.sample_position["name"])
        self.assertEqual(data["start_year"], self.sample_position["start_year"])
        self.assertEqual(data["salary"], self.sample_position["salary"])
        self.assertIn("id", data)
        mock_create.assert_called_once()
    
    @patch('src.services.position_service.position_service.create')
    def test_create_position_service_error(self, mock_create):
        """Test position creation when service raises exception"""
        mock_create.side_effect = Exception("Database error")
        
        response = self.client.post("/api/positions/", json=self.sample_position)
        
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("Failed to create position", data["detail"])
    
    def test_create_position_invalid_dates(self):
        """Test position creation with invalid date values"""
        invalid_position = {
            **self.sample_position,
            "start_month": 13  # Invalid month
        }
        
        response = self.client.post("/api/positions/", json=invalid_position)
        
        self.assertEqual(response.status_code, 422)
        data = response.json()
        self.assertIn("detail", data)
    
    def test_create_position_invalid_year_range(self):
        """Test position creation with year outside valid range"""
        invalid_position = {
            **self.sample_position,
            "start_year": 1800  # Too early
        }
        
        response = self.client.post("/api/positions/", json=invalid_position)
        
        self.assertEqual(response.status_code, 422)
    
    def test_create_position_missing_required_fields(self):
        """Test position creation with missing required fields"""
        invalid_position = {
            "start_year": 2023,
            "start_month": 1
            # Missing name, start_day
        }
        
        response = self.client.post("/api/positions/", json=invalid_position)
        
        self.assertEqual(response.status_code, 422)
    
    def test_create_position_with_details(self):
        """Test position creation with nested details"""
        position_with_details = {
            **self.sample_position,
            "details": [
                {
                    "id": 1,
                    "name": "Test Detail",
                    "description": {"type": "doc", "content": []},
                    "tags": [],
                    "details": []
                }
            ]
        }
        
        response_data = {
            **self.sample_position_response,
            "details": position_with_details["details"]
        }
        
        with patch('src.services.position_service.position_service.create') as mock_create:
            mock_position = Position(**response_data)
            mock_create.return_value = mock_position
            
            response = self.client.post("/api/positions/", json=position_with_details)
            
            self.assertEqual(response.status_code, 201)
            data = response.json()
            self.assertEqual(len(data["details"]), 1)
            self.assertEqual(data["details"][0]["name"], "Test Detail")
    
    @patch('src.services.position_service.position_service.get_all')
    def test_get_all_positions_success(self, mock_get_all):
        """Test successful retrieval of all positions"""
        mock_positions = [Position(**self.sample_position_response)]
        mock_get_all.return_value = mock_positions
        
        response = self.client.get("/api/positions/")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], self.sample_position["name"])
        mock_get_all.assert_called_once()
    
    @patch('src.services.position_service.position_service.get_all')
    def test_get_all_positions_empty(self, mock_get_all):
        """Test retrieval when no positions exist"""
        mock_get_all.return_value = []
        
        response = self.client.get("/api/positions/")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)
    
    @patch('src.services.position_service.position_service.get_by_id')
    def test_get_position_by_id_success(self, mock_get_by_id):
        """Test successful retrieval of position by ID"""
        mock_position = Position(**self.sample_position_response)
        mock_get_by_id.return_value = mock_position
        
        response = self.client.get("/api/positions/1")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["name"], self.sample_position["name"])
        mock_get_by_id.assert_called_once_with(1)
    
    @patch('src.services.position_service.position_service.get_by_id')
    def test_get_position_by_id_not_found(self, mock_get_by_id):
        """Test retrieval of non-existent position"""
        mock_get_by_id.return_value = None
        
        response = self.client.get("/api/positions/999")
        
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data["detail"], "Position not found")
    
    @patch('src.services.position_service.position_service.update')
    def test_update_position_success(self, mock_update):
        """Test successful position update"""
        updated_position_data = {
            **self.sample_position_response,
            "name": "Updated Position Name",
            "salary": 85000.0
        }
        mock_position = Position(**updated_position_data)
        mock_update.return_value = mock_position
        
        update_data = {"name": "Updated Position Name", "salary": 85000.0}
        response = self.client.put("/api/positions/1", json=update_data)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Updated Position Name")
        self.assertEqual(data["salary"], 85000.0)
        self.assertEqual(data["id"], 1)
        mock_update.assert_called_once()
    
    @patch('src.services.position_service.position_service.update')
    def test_update_position_not_found(self, mock_update):
        """Test update of non-existent position"""
        mock_update.return_value = None
        
        update_data = {"name": "Updated Position Name"}
        response = self.client.put("/api/positions/999", json=update_data)
        
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data["detail"], "Position not found")
    
    def test_update_position_invalid_data(self):
        """Test position update with invalid data"""
        invalid_update = {"start_month": 15}  # Invalid month
        
        response = self.client.put("/api/positions/1", json=invalid_update)
        
        self.assertEqual(response.status_code, 422)
    
    @patch('src.services.position_service.position_service.delete')
    def test_delete_position_success(self, mock_delete):
        """Test successful position deletion"""
        mock_delete.return_value = True
        
        response = self.client.delete("/api/positions/1")
        
        self.assertEqual(response.status_code, 204)
        mock_delete.assert_called_once_with(1)
    
    @patch('src.services.position_service.position_service.delete')
    def test_delete_position_not_found(self, mock_delete):
        """Test deletion of non-existent position"""
        mock_delete.return_value = False
        
        response = self.client.delete("/api/positions/999")
        
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data["detail"], "Position not found")

if __name__ == '__main__':
    unittest.main()