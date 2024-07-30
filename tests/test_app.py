import unittest
from app import app, save_preferences, load_preferences, get_chatgpt_recommendations, validate_input
from app import User, Book, Movie, Song

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        """Set up the test client and other resources before each test."""
        self.app = app.test_client()
        self.app.testing = True
        self.test_user = User("testuser")

    def tearDown(self):
        """Clean up after each test."""
        pass  # Add cleanup code here if necessary

    def test_index_page(self):
        """Test that the index page loads correctly."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)

    def test_add_user(self):
        """Test adding a user via POST request."""
        with self.app as c:
            response = c.post('/add_user', data={'username': 'testuser'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Welcome testuser!', response.data)
            # Check if user is set in session
            with c.session_transaction() as sess:
                self.assertEqual(sess['current_user'], 'testuser')

    def test_add_preference(self):
        """Test adding a preference and ensure it's saved correctly."""
        self.test_user.add_preference('books', Book('Test Book', 'Fiction', 'Author A'))
        save_preferences(self.test_user.name, self.test_user.preferences)
        loaded_preferences = load_preferences(self.test_user.name)
        self.assertIn({'title': 'Test Book', 'genre': 'Fiction', 'author': 'Author A'}, loaded_preferences['books'])

    def test_get_chatgpt_recommendations(self):
        """Test the ChatGPT recommendation function."""
        preferences = {
            'books': [{'title': 'Test Book', 'genre': 'Fiction', 'author': 'Author A'}],
            'movies': [{'title': 'Test Movie', 'genre': 'Action', 'director': 'Director B'}],
            'songs': [{'title': 'Test Song', 'genre': 'Pop', 'artist': 'Artist C'}]
        }
        recommendations = get_chatgpt_recommendations(preferences)
        self.assertIn('Based on', recommendations)

    def test_save_and_load_preferences(self):
        """Test saving and loading user preferences."""
        self.test_user.add_preference('books', Book('Another Test Book', 'Sci-Fi', 'Author B'))
        save_preferences(self.test_user.name, self.test_user.preferences)
        loaded_preferences = load_preferences(self.test_user.name)
        self.assertEqual(self.test_user.preferences, loaded_preferences)

    def test_validate_input(self):
        """Test input validation function."""
        valid_data = validate_input('books', ['books', 'movies', 'songs'])
        self.assertEqual(valid_data, 'books')
        with self.assertRaises(ValueError):
            validate_input('invalid_category', ['books', 'movies', 'songs'])

if __name__ == '__main__':
    unittest.main()