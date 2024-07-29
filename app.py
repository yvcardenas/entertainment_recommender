from flask import Flask, render_template, request, redirect, url_for, session
import json
import openai
import os

app = Flask(__name__, template_folder='./html')
app.secret_key = 'supersecretkey'
user_data_path = 'user_data'

# Ensure user_data directory exists
os.makedirs(user_data_path, exist_ok=True)

# Placeholder for OpenAI key and function
openai.api_key = 'INSERT API KEY HERE'

def get_chatgpt_recommendations(preferences):
    # Implement the function using OpenAI API
    prompt = "Based on the following preferences, recommend one book, one movie, and one song:\n"
    for category, items in preferences.items():
        prompt += f"{category.capitalize()}:\n"
        prompt += ''.join([f" - {item['title']} ({item['genre']})\n" for item in items])

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
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

@app.route('/', methods=['GET', 'POST'])
def index():
    current_user = session.get('current_user')
    user_preferences= None

    if current_user:
        user_preferences = load_preferences(current_user)

    if request.method == 'POST':
        username = request.form['username']
        session['current_user'] = username
        return redirect(url_for('index'))
    
    return render_template('index.html', current_user=current_user, user_preferences=user_preferences)

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

    if not any(user_preferences.values()):
        message = "No preferences found. Please add some preferences first."
        return render_template('recommendations.html', message=message)
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

if __name__ == '__main__':
    app.run(debug=True)
