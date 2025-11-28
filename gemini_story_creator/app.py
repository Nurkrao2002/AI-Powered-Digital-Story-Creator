import os
import random
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY and API_KEY != "your_api_key_here":
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_story():
    data = request.json
    title = data.get('title')
    prompt = data.get('prompt')
    characters = data.get('characters')
    style = data.get('style')
    length = data.get('length')

    # Construct the prompt for AI
    length_prompt = length
    if length == "Unlimited":
        length_prompt = "an extremely long, highly detailed, and extensive epic. Elaborate on every scene, character thought, and dialogue. Write multiple chapters if possible. The story should be as long as the model allows."

    full_prompt = (
        f"Write a {length_prompt} story titled '{title}'. "
        f"The story should be about: {prompt}. "
        f"Characters involved: {characters}. "
        f"Writing style: {style}. "
        "Make it engaging and suitable for a general audience."
    )

    story = ""
    source = "AI"

    if model:
        try:
            response = model.generate_content(full_prompt)
            story = response.text
        except Exception as e:
            print(f"Error generating story with AI: {e}")
            story = generate_fallback_story(title, characters, prompt, length)
            source = "Fallback (AI Error)"
    else:
        story = generate_fallback_story(title, characters, prompt, length)
        source = "Fallback (No API Key)"

    return jsonify({'story': story, 'source': source})

def generate_fallback_story(title, characters, prompt, length="Short"):
    """A simple template-based generator when AI is unavailable."""
    chars = characters.split(',') if characters else ['our hero']
    main_char = chars[0].strip()
    
    base_story = [
        f"Once upon a time, {main_char} embarked on a great adventure. The goal was simple: {prompt}.",
        f"Along the way, many challenges arose. The path was treacherous, filled with obstacles that tested {main_char}'s courage.",
        f"With determination, {main_char} overcame them all. Friends were made, enemies were defeated, and lessons were learned.",
        f"In the end, it was a journey worth remembering. The legend of {title} would be told for generations."
    ]

    if length == "Unlimited" or length == "Long":
        # Extend the story for longer requests in fallback mode
        extension = [
            f"But the story didn't end there. {main_char} realized that this was just the beginning.",
            f"New lands were discovered beyond the horizon. Mysteries that had slept for centuries were awakened.",
            f"Every day brought a new adventure, a new puzzle to solve. {main_char} grew stronger and wiser with each passing moment.",
            f"The world was vast, and {main_char} wanted to see it all. From the highest peaks to the deepest oceans, the journey continued forever."
        ]
        base_story.extend(extension)
    
    return " ".join(base_story)

if __name__ == '__main__':
    app.run(debug=True)
