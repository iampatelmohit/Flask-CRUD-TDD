import unittest
import app  # Import the whole file to keep the database "Live"

class TestAPI(unittest.TestCase):
    
    def setUp(self):
        # 1. Configure the app for testing
        app.app.config['TESTING'] = True
        self.client = app.app.test_client()
        
        # 2. Reset the Database
        # We access 'app.comments_db' directly so we always get the latest list
        # even if the app replaced it during the last test.
        if hasattr(app, 'comments_db'):
            app.comments_db.clear()
            app.comments_db.append({'id': 1, 'task_id': 1, 'text': 'Initial Comment', 'author': 'System'})

    # Test 1: Get Comments
    def test_get_comments(self):
        response = self.client.get('/tasks/1/comments')
        self.assertEqual(response.status_code, 200)
        # Verify the text is inside the response
        self.assertIn(b"Initial Comment", response.data)

    # Test 2: Add Comment
    def test_add_comment(self):
        new_data = {'text': 'Testing with Unittest', 'author': 'Robot'}
        response = self.client.post('/tasks/1/comments', 
                                    json=new_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"Testing with Unittest", response.data)

    # Test 3: Delete Comment
    def test_delete_comment(self):
        # Delete the comment we added in setUp
        response = self.client.delete('/comments/1')
        self.assertEqual(response.status_code, 204)
        
        # Verify it is gone
        response = self.client.get('/tasks/1/comments')
        self.assertNotIn(b"Initial Comment", response.data)

if __name__ == '__main__':
    unittest.main()