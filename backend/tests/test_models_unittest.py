import unittest
from pydantic import ValidationError
from src.models.entity import Entity, EntityCreate, EntityUpdate
from src.models.position import Position, PositionCreate, PositionUpdate, DetailBase
from datetime import datetime

class TestEntityModels(unittest.TestCase):
    """Test cases for Entity Pydantic models"""
    
    def setUp(self):
        """Set up sample data"""
        self.valid_entity_data = {
            "id": 1,
            "name": "Test Entity",
            "entity_type": "skill",
            "entity_parent": None,
            "color": "#ff0000",
            "icon": "test-icon",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
    
    def test_entity_model_valid(self):
        """Test Entity model with valid data"""
        entity = Entity(**self.valid_entity_data)
        
        self.assertEqual(entity.name, "Test Entity")
        self.assertEqual(entity.entity_type, "skill")
        self.assertEqual(entity.id, 1)
        self.assertIsInstance(entity.created_at, datetime)
        self.assertIsInstance(entity.updated_at, datetime)
    
    def test_entity_create_valid(self):
        """Test EntityCreate model with valid data"""
        create_data = {
            "name": "New Entity",
            "entity_type": "tool",
            "color": "#00ff00"
        }
        entity_create = EntityCreate(**create_data)
        
        self.assertEqual(entity_create.name, "New Entity")
        self.assertEqual(entity_create.entity_type, "tool")
        self.assertEqual(entity_create.color, "#00ff00")
    
    def test_entity_create_invalid_type(self):
        """Test EntityCreate with invalid entity_type"""
        invalid_data = {
            "name": "Test Entity",
            "entity_type": "invalid_type"
        }
        
        with self.assertRaises(ValidationError) as context:
            EntityCreate(**invalid_data)
        
        self.assertIn("entity_type", str(context.exception))
    
    def test_entity_create_missing_name(self):
        """Test EntityCreate with missing required name"""
        invalid_data = {
            "entity_type": "skill"
        }
        
        with self.assertRaises(ValidationError) as context:
            EntityCreate(**invalid_data)
        
        self.assertIn("name", str(context.exception))
    
    def test_entity_create_empty_name(self):
        """Test EntityCreate with empty name"""
        invalid_data = {
            "name": "",
            "entity_type": "skill"
        }
        
        with self.assertRaises(ValidationError) as context:
            EntityCreate(**invalid_data)
        
        self.assertIn("at least 1 character", str(context.exception))
    
    def test_entity_create_name_too_long(self):
        """Test EntityCreate with name exceeding max length"""
        invalid_data = {
            "name": "x" * 101,  # Exceeds 100 character limit
            "entity_type": "skill"
        }
        
        with self.assertRaises(ValidationError) as context:
            EntityCreate(**invalid_data)
        
        self.assertIn("at most 100 character", str(context.exception))
    
    def test_entity_update_partial(self):
        """Test EntityUpdate with partial data"""
        update_data = {
            "name": "Updated Name"
        }
        entity_update = EntityUpdate(**update_data)
        
        self.assertEqual(entity_update.name, "Updated Name")
        self.assertIsNone(entity_update.entity_type)
        self.assertIsNone(entity_update.color)
    
    def test_entity_update_empty(self):
        """Test EntityUpdate with no data"""
        entity_update = EntityUpdate()
        
        self.assertIsNone(entity_update.name)
        self.assertIsNone(entity_update.entity_type)
        self.assertIsNone(entity_update.color)
    
    def test_entity_valid_types(self):
        """Test all valid entity types"""
        valid_types = [
            "company", "person", "skill", "location", "room", 
            "container", "equipment", "muscles", "meta", 
            "exercise_type", "object", "tool", "other"
        ]
        
        for entity_type in valid_types:
            create_data = {
                "name": f"Test {entity_type}",
                "entity_type": entity_type
            }
            entity = EntityCreate(**create_data)
            self.assertEqual(entity.entity_type, entity_type)


class TestPositionModels(unittest.TestCase):
    """Test cases for Position Pydantic models"""
    
    def setUp(self):
        """Set up sample data"""
        self.valid_position_data = {
            "id": 1,
            "name": "Test Position",
            "start_year": 2023,
            "start_month": 1,
            "start_day": 15,
            "end_year": 2024,
            "end_month": 6,
            "end_day": 30,
            "salary": 75000.0,
            "details": [],
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
    
    def test_position_model_valid(self):
        """Test Position model with valid data"""
        position = Position(**self.valid_position_data)
        
        self.assertEqual(position.name, "Test Position")
        self.assertEqual(position.start_year, 2023)
        self.assertEqual(position.start_month, 1)
        self.assertEqual(position.salary, 75000.0)
        self.assertEqual(position.id, 1)
    
    def test_position_create_valid(self):
        """Test PositionCreate model with valid data"""
        create_data = {
            "name": "New Position",
            "start_year": 2023,
            "start_month": 6,
            "start_day": 1,
            "salary": 80000.0,
            "details": []
        }
        position_create = PositionCreate(**create_data)
        
        self.assertEqual(position_create.name, "New Position")
        self.assertEqual(position_create.start_year, 2023)
        self.assertEqual(position_create.salary, 80000.0)
    
    def test_position_create_missing_required(self):
        """Test PositionCreate with missing required fields"""
        invalid_data = {
            "start_year": 2023,
            "start_month": 1
            # Missing name and start_day
        }
        
        with self.assertRaises(ValidationError) as context:
            PositionCreate(**invalid_data)
        
        error_str = str(context.exception)
        self.assertIn("name", error_str)
        self.assertIn("start_day", error_str)
    
    def test_position_invalid_year_range(self):
        """Test Position with year outside valid range"""
        invalid_data = {
            "name": "Test Position",
            "start_year": 1800,  # Too early
            "start_month": 1,
            "start_day": 1
        }
        
        with self.assertRaises(ValidationError) as context:
            PositionCreate(**invalid_data)
        
        self.assertIn("greater than or equal to 1900", str(context.exception))
    
    def test_position_invalid_month(self):
        """Test Position with invalid month"""
        invalid_data = {
            "name": "Test Position",
            "start_year": 2023,
            "start_month": 13,  # Invalid month
            "start_day": 1
        }
        
        with self.assertRaises(ValidationError) as context:
            PositionCreate(**invalid_data)
        
        self.assertIn("less than or equal to 12", str(context.exception))
    
    def test_position_invalid_day(self):
        """Test Position with invalid day"""
        invalid_data = {
            "name": "Test Position",
            "start_year": 2023,
            "start_month": 1,
            "start_day": 32  # Invalid day
        }
        
        with self.assertRaises(ValidationError) as context:
            PositionCreate(**invalid_data)
        
        self.assertIn("less than or equal to 31", str(context.exception))
    
    def test_position_negative_salary(self):
        """Test Position with negative salary"""
        invalid_data = {
            "name": "Test Position",
            "start_year": 2023,
            "start_month": 1,
            "start_day": 1,
            "salary": -1000.0
        }
        
        with self.assertRaises(ValidationError) as context:
            PositionCreate(**invalid_data)
        
        self.assertIn("greater than or equal to 0", str(context.exception))
    
    def test_position_end_year_validation(self):
        """Test Position end year validation"""
        # This would require custom validator implementation
        # For now, just test that the model accepts valid end dates
        valid_data = {
            "name": "Test Position",
            "start_year": 2023,
            "start_month": 1,
            "start_day": 1,
            "end_year": 2024,
            "end_month": 6,
            "end_day": 30
        }
        
        position = PositionCreate(**valid_data)
        self.assertEqual(position.end_year, 2024)
    
    def test_position_update_partial(self):
        """Test PositionUpdate with partial data"""
        update_data = {
            "name": "Updated Position",
            "salary": 90000.0
        }
        position_update = PositionUpdate(**update_data)
        
        self.assertEqual(position_update.name, "Updated Position")
        self.assertEqual(position_update.salary, 90000.0)
        self.assertIsNone(position_update.start_year)
    
    def test_detail_base_model(self):
        """Test DetailBase model"""
        detail_data = {
            "id": 1,
            "name": "Test Detail",
            "description": {"type": "doc", "content": []},
            "tags": [],
            "details": []
        }
        
        detail = DetailBase(**detail_data)
        self.assertEqual(detail.name, "Test Detail")
        self.assertEqual(detail.id, 1)
        self.assertIsInstance(detail.description, dict)
        self.assertIsInstance(detail.tags, list)
        self.assertIsInstance(detail.details, list)
    
    def test_detail_base_nested(self):
        """Test DetailBase with nested details"""
        nested_detail_data = {
            "id": 1,
            "name": "Parent Detail",
            "description": {},
            "tags": [],
            "details": [
                {
                    "id": 2,
                    "name": "Child Detail",
                    "description": {},
                    "tags": [],
                    "details": []
                }
            ]
        }
        
        detail = DetailBase(**nested_detail_data)
        self.assertEqual(len(detail.details), 1)
        self.assertEqual(detail.details[0].name, "Child Detail")
        self.assertEqual(detail.details[0].id, 2)

if __name__ == '__main__':
    unittest.main()