# Entertainment Recommender
## Overview
The Entertainment Recommender is a Flask-based web application that suggests books, movies, and songs based on user preferences. By leveraging OpenAI’s GPT-3.5-turbo model, the application generates personalized recommendations to enhance your entertainment experience.

## Features
-	**User Preferences**: Users can input their favorite books, movies, and songs along with their genres.
-	**Personalized Recommendations**: The app generates recommendations based on the user’s preferences using the OpenAI API.
-	**User-Friendly Interface**: A clean and intuitive interface makes it easy for users to add preferences and view recommendations.

## Installations
1. **Clone the respository**:
     ```bash
    git clone https://github.com/yourusername/entertainment_recommender.git
    cd entertainment_recommender
    ```
2. **Create a Virtual Environment**:
     ```bash
    python3 -m venv venv
    source venv/bin/activate 
    ```
3. **Install Dependencies**:
     ```bash
    pip install -r requirements.txt
    ```
4. **Set Up OpenAI API Key**:
     ```
     OPENAI_API_KEY=your_openai_api_key
     ```
5. **Run the Application**:
     ```bash
     flask --app app run --port 5002 --host 0.0.0.0 --debug
     ```
## Usage

1. **Set a User**:
   - Start by entering a username to set your session.
   
2. **Add Preferences**:
   - Add your favorite books, movies, and songs along with their genres. This information will be used to generate recommendations.

3. **Get Recommendations**:
   - Navigate to the recommendations page to view personalized suggestions for books, movies, and songs based on your preferences.

## File Structure
- **app.py**: The main application file containing Flask routes and logic.
- **templates/**: Directory containing HTML templates for the application.
  - `index.html`: The homepage where users can set their username and view current preferences.
  - `add_preference.html`: The page where users can add their entertainment preferences.
  - `recommendations.html`: The page displaying the generated recommendations.
- **static/**: Directory for static files like CSS.
  - `style.css`: The main stylesheet for the application.
- **requirements.txt**: List of dependencies required to run the application.

## Technologies Used
- **Flask**: A lightweight WSGI web application framework in Python.
- **OpenAI API**: Utilized for generating entertainment recommendations.
- **HTML/CSS**: Frontend structure and styling.

## Contact

For questions or feedback, please reach out at [ygcrds@gmail.com].
