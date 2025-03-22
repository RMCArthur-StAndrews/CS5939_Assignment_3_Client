import unittest
from unittest.mock import patch, Mock
from Controllers.ServiceCheck import CloudBackendChecker
from io import StringIO
import sys
import time
import os

class TestCloudBackendChecker(unittest.TestCase):
    @patch('requests.get')
    @patch.dict(os.environ, {}, clear=True)
    def test_backend_running(self, mock_get):
        # Mock the response to simulate the backend running
        mock_response = Mock()
        mock_response.json.return_value = {'error': 200}
        mock_get.return_value = mock_response

        checker = CloudBackendChecker("http://127.0.0.1:5000/utils")

        # Redirect stdout to capture print statements
        captured_output = StringIO()
        sys.stdout = captured_output

        # Start the checker thread
        checker.start()
        time.sleep(20)  # Wait for the thread to execute

        # Stop the checker thread
        checker.stop()
        checker.join()

        # Reset redirect.
        sys.stdout = sys.__stdout__

        mock_get.assert_called_with("http://127.0.0.1:5000/utils")
        self.assertIn("Cloud backend is running", captured_output.getvalue())
        self.assertEqual(os.environ.get("LOCAL_MODE"), "False")

    @patch('requests.get')
    @patch.dict(os.environ, {}, clear=True)
    def test_backend_not_running(self, mock_get):
        # Mock the response to simulate the backend not running
        mock_response = Mock()
        mock_response.json.return_value = {'error': 400}
        mock_get.return_value = mock_response

        checker = CloudBackendChecker("http://10.0.0.3:5000/utils")

        # Redirect stdout to capture print statements
        captured_output = StringIO()
        sys.stdout = captured_output

        # Start the checker thread
        checker.start()
        time.sleep(20)  # Wait for the thread to execute

        # Stop the checker thread
        checker.stop()
        checker.join()

        # Reset redirect.
        sys.stdout = sys.__stdout__

        mock_get.assert_called_with("http://10.0.0.3:5000/utils")
        self.assertIn("Cloud backend is not running", captured_output.getvalue())
        self.assertEqual(os.environ.get("LOCAL_MODE"), "True")

if __name__ == '__main__':
    unittest.main()