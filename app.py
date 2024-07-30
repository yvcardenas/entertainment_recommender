from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import json
import openai
import os

# Initialize the Flask app and OpenAI API key
app = Flask(__name__, template_folder='./templates')
app.secret_key = 'supersecretkey' # Secret key for session management
user_data_path = 'user_data' # Dictionary to store user preferences

# Load environment variables from .env file 
load_dotenv()
# Ensure user_data directory exists
os.makedirs(user_data_path, exist_ok=True)

# Placeholder for OpenAI key and function
openai.api_key = os.getenv('OPENAI_API_KEY')

# Base class for Entertainment items
class Entertainment:
    def __init__(self, title, genre):
        self.title = title
        self.genre = genre

    def to_dict(self):
        return {'title': self.title, 'genre': self.genre}

# Subclass for books, inheriting from Entertainment
class Book(Entertainment):
    def __init__(self, title, genre, author):
        super().__init__(title, genre)
        self.author = author

    def to_dict(self):
        data = super().to_dict()
        data['author'] = self.author
        return data

# Subclass for movies, inheriting from Entertainment
class Movie(Entertainment):
    def __init__(self, title, genre, director):
        super().__init__(title, genre)
        self.director = director

    def to_dict(self):
        data = super().to_dict()
        data['director'] = self.director
        return data

# Subclass for songs, inheriting from Entertainment
class Song(Entertainment):
    def __init__(self, title, genre, artist):
        super().__init__(title, genre)
        self.artist = artist

    def to_dict(self):
        data = super().to_dict()
        data['artist'] = self.artist
        return data

# User class to manage user preferences and interactions
class User:
    def __init__(self, name):
        self.name = name
        self.preferences = {'books': [], 'movies': [], 'songs': []}

    def add_preference(self, category, item):
        # Adds a preference to the user's list
        if category not in self.preferences:
            self.preferences[category] = []
        self.preferences[category].append(item.to_dict())

    def get_recommendations(self):
        # Generates recommendations user's preferences in a readable format
        return get_chatgpt_recommendations(self.preferences)

    def display_preferences(self):
        # Displays the user's preferences in a readble format.
        display = f"User: {self.name}\nPreferences:\n"
        for category, items in self.preferences.items():
            display += f"{category.capitalize()}:\n"
            for item in items:
                details = ", ".join([f"{key}: {value}" for key, value in item.items() if key != 'title'])
                display += f"  - {item['title']} ({details})\n"
        return display

# Function to get recommendations from ChatGPT
def get_chatgpt_recommendations(preferences):
    prompt = "Based on the following preferences, recommend one book, one movie, and one song. Use this example as a format\'Based on the romance genre preference, here are some recommendations for you:\n\nBook: \"Pride and Prejudice\" by Jane Austen - A classic romance novel with a strong female protagonist and a timeless love story.\n\nMovie: \"The Notebook\" - A romantic drama that tells the story of a young couple\'s love and the challenges they face as they grow older.\n\nSong: \"Perfect\" by Ed Sheeran - A beautiful love song that captures the feeling of finding someone who is perfect for you.\':\n"
    for category, items in preferences.items():
        prompt += f"{category.capitalize()}:\n"
        prompt += ''.join([f" - {item['title']} ({item['genre']})\n" for item in items])
    
    print("Prompt: ", prompt)

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.5
        )
        print("API Response:", response)
        if response.choices and len(response.choices) > 0:
            recommendations = response.choices[0].message.content
        else:
            recommendations = "No recommendations available."
    except Exception as e:
        print(f"Error getting recommendations: {e}")
        recommendations = "An error occurred while getting recommendations."
    return recommendations

# Function to validate user input
def validate_input(data, valid_options=None):
    if valid_options and data not in valid_options:
        raise ValueError(f"Invalid input: {data}. Expected one of {valid_options}.")
    return data

# Function to save user preferences to a file
def save_preferences(username, preferences):
    filename = os.path.join(user_data_path, f'{username}_preferences.json')
    with open(filename, "w") as file:
        json.dump(preferences, file)

# Function to load user preferences from a file
def load_preferences(username):
    filename = os.path.join(user_data_path, f'{username}_preferences.json')
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return {'books': [], 'movies': [], 'songs': []}

# Route for index page
@app.route('/', methods=['GET', 'POST'])
def index():
    # Handles the main page, allowing users to log in and view their preferences
    current_user = session.get('current_user')
    user_preferences= load_preferences(current_user) if current_user else None

    if request.method == 'POST':
        username = request.form['username']
        session['current_user'] = username
        return redirect(url_for('index'))
    
    return render_template('index.html', current_user=current_user, user_preferences=user_preferences)

# Route for adding a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    # Adds a new user to the session
    username = request.form['username']
    session['current_user'] = username
    return redirect(url_for('index'))

# Route for adding a new preference
@app.route('/add_preference', methods=['GET', 'POST'])
def add_preference():
    # if 'curent_user' not in session:
    #     return redirect(url_for('index'))
    
    if request.method == 'POST':
        category = request.form['category']
        title = request.form['title']
        genre = request.form['genre']
        extra = request.form['extra']
        validate_input(category, ['books', 'movies', 'songs'])
        
        current_user = session['current_user']
        user_preferences = load_preferences(current_user)

        if category == 'books':
            user_preferences['books'].append(Book(title, genre, extra).to_dict())
        elif category == 'movies':
            user_preferences['movies'].append(Movie(title, genre, extra).to_dict())
        elif category == 'songs':
            user_preferences['songs'].append(Song(title, genre, extra).to_dict())

        save_preferences(current_user, user_preferences)
        return redirect(url_for('index'))
    return render_template('add_preference.html')

# Route for generating and displaying recommendations
@app.route('/recommendations')
def recommendations():
    if 'current_user' not in session:
        return redirect(url_for('index'))

    current_user = session['current_user']
    user_preferences = load_preferences(current_user)

    if not any(user_preferences.values()):
        return render_template('recommendations.html', message="No preferences found. Please add some preferences first.")
    
    recommendations = get_chatgpt_recommendations(user_preferences)
    return render_template('recommendations.html', recommendations=recommendations)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
