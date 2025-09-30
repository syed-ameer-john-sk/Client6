import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the Python path to allow for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from classes import generate_run_number

class TestGenerateRunNumber(unittest.TestCase):

    @patch('classes.get_db_connection')
    def test_generate_run_number_with_malformed_data(self, mock_get_db_connection):
        # Arrange
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            ('PROJ-TASK-abc',),  # Malformed run number
            ('PROJ-TASK-002',),  # Valid run number
            ('PROJ-TASK-001',)   # Older valid run number
        ]

        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_connection

        project_code = 'PROJ'
        task_code = 'TASK'

        # Act
        result = generate_run_number(project_code, task_code)

        # Assert
        self.assertEqual(result, 'PROJ-TASK-003')

    @patch('classes.get_db_connection')
    def test_generate_run_number_with_no_existing_runs(self, mock_get_db_connection):
        # Arrange
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []

        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_connection

        project_code = 'PROJ'
        task_code = 'TASK'

        # Act
        result = generate_run_number(project_code, task_code)

        # Assert
        self.assertEqual(result, 'PROJ-TASK-001')

    @patch('classes.get_db_connection')
    def test_generate_run_number_all_malformed(self, mock_get_db_connection):
        # Arrange
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            ('PROJ-TASK-abc',),
            ('PROJ-TASK-def',),
        ]

        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_connection

        project_code = 'PROJ'
        task_code = 'TASK'

        # Act
        result = generate_run_number(project_code, task_code)

        # Assert
        self.assertEqual(result, 'PROJ-TASK-001')

if __name__ == '__main__':
    unittest.main()