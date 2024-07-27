from flask import Flask, render_template, request, redirect, url_for, session
import json
import openai
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
user_data_path = 'user_data'

# Ensure user_data directory exists
os.makedirs(user_data_path, exist_ok=True)

# Placeholder for your OpenAI key and function
openai_api_key = 'your_openai_api_key'
openai.api_key = openai_api_key

def get_chatgpt_recommendations(preferences):
    # Implement the function using OpenAI API
    prompt = "Based on the following preferences, recommend a book, movie, and song:\n"
    for category, items in preferences.items():
        prompt += f"{category.capitalize()}:\n"
        prompt += ''.join([f" - {item['title']} ({item['genre']})\n" for item in items])

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    recommendations = response.choices[0].text.strip()
    return recommendations

@app.route('/')
def index():
    current_user = session.get('current_user')
    return render_template('index.html', current_user=current_user)

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    session['current_user'] = username
    return redirect(url_for('index'))

@app.route('/add_preference', methods=['GET', 'POST'])
def add_preference():
    if request.method == 'POST':
        category = request.form['category']
        title = request.form['title']
        genre = request.form['genre']
        extra = request.form['extra']
        
        if 'current_user' not in session:
            return redirect(url_for('index'))
        
        current_user = session['current_user']
        user_preferences = load_preferences(current_user)
        if category == 'books':
            user_preferences['books'].append({'title': title, 'genre': genre, 'author': extra})
        elif category == 'movies':
            user_preferences['movies'].append({'title': title, 'genre': genre, 'director': extra})
        elif category == 'songs':
            user_preferences['songs'].append({'title': title, 'genre': genre, 'artist': extra})

        save_preferences(current_user, user_preferences)
        return redirect(url_for('index'))
    return render_template('add_preference.html')

@app.route('/recommendations')
def recommendations():
    if 'current_user' not in session:
        return redirect(url_for('index'))

    current_user = session['current_user']
    user_preferences = load_preferences(current_user)
    recommendations = get_chatgpt_recommendations(user_preferences)
    return render_template('recommendations.html', recommendations=recommendations)

def save_preferences(username, preferences):
    filename = os.path.join(user_data_path, f'{username}_preferences.json')
    with open(filename, "w") as file:
        json.dump(preferences, file)

def load_preferences(username):
    filename = os.path.join(user_data_path, f'{username}_preferences.json')
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return {'books': [], 'movies': [], 'songs': []}

# if __name__ == '__main__':
#     app.run(debug=True)