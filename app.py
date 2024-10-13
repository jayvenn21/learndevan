import base64
import io
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from flask import Flask, render_template, jsonify, request
import random
import speech_recognition as sr
from PIL import Image
from gtts import gTTS  # Import the gTTS library

app = Flask(__name__)

# Load the pre-trained Devanagari character model
model = load_model('devanagari.keras')

# Define the Devanagari class labels
letter_count = {
    0: 'CHECK', 1: '01_ka', 2: '02_kha', 3: '03_ga', 4: '04_gha', 5: '05_kna',
    6: '06_cha', 7: '07_chha', 8: '08_ja', 9: '09_jha', 10: '10_yna',
    11: '11_taa', 12: '12_thaa', 13: '13_daa', 14: '14_dhaa', 15: '15_adna',
    16: '16_ta', 17: '17_tha', 18: '18_da', 19: '19_dha', 20: '20_na',
    21: '21_pa', 22: '22_pha', 23: '23_ba', 24: '24_bha', 25: '25_ma',
    26: '26_yaw', 27: '27_ra', 28: '28_la', 29: '29_waw', 30: '30_saw',
    31: '31_petchiryakha', 32: '32_patalosaw', 33: '33_ha', 34: '34_chhya',
    35: '35_tra', 36: '36_gya', 37: 'CHECK'
}

# Define the phonetic spelling for each character with Hindi characters
phonetic_spelling = {
    0: 'CHECK', 
    1: 'का (ka)', 
    2: 'खा (kha)', 
    3: 'गा (ga)', 
    4: 'घा (gha)', 
    5: 'क्ना (kna)',
    6: 'चा (cha)', 
    7: 'छा (chha)', 
    8: 'जा (ja)', 
    9: 'झा (jha)', 
    10: 'यना (yna)',
    11: 'ता (taa)', 
    12: 'था (thaa)', 
    13: 'दा (daa)', 
    14: 'धा (dhaa)', 
    15: 'अदना (adna)',
    16: 'ता (ta)', 
    17: 'था (tha)', 
    18: 'दा (da)', 
    19: 'धा (dha)', 
    20: 'ना (na)',
    21: 'पा (pa)', 
    22: 'फा (pha)', 
    23: 'बा (ba)', 
    24: 'भा (bha)', 
    25: 'मा (ma)',
    26: 'यव (yaw)', 
    27: 'रा (ra)', 
    28: 'ला (la)', 
    29: 'वव (waw)', 
    30: 'सव (saw)',
    31: 'पेचिर्यखा (petchiryakha)', 
    32: 'पटलोसव (patalosaw)', 
    33: 'हा (ha)', 
    34: 'छ्या (chhya)',
    35: 'त्र (tra)', 
    36: 'ज्ञ (gya)', 
    37: 'CHECK'
}

# Language dictionary mapping languages to Google Speech API language codes
LANGUAGES = {
    "English (US)": "en-US",
    "Hindi": "hi-IN",
    "Telugu": "te-IN"
}

# Speech Recognition Function
def recognize_speech(language_code):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"Listening in {language_code}...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language=language_code)
            print(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError:
            return "Request error from speech recognition service"

# Image preparation for character recognition
def prepare_image(image):
    img_array = np.array(image.convert("L"))  # Convert to grayscale
    new_array = Image.fromarray(img_array).resize((32, 32))  # Resize to 32x32 for the Devanagari model
    return np.array(new_array).reshape(-1, 32, 32, 1) / 255.0  # Normalize and reshape

@app.route('/')
def index():
    return render_template('index.html')

# Function to convert text to speech and save it as an audio file
def text_to_speech(pronunciation, character):
    # Create the audio directory if it doesn't exist
    audio_dir = 'static/audio'
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)  # Create the directory

    # Create a unique filename for the pronunciation audio
    filename = f'{audio_dir}/{character}.mp3'
    if not os.path.exists(filename):  # Check if the file already exists
        tts = gTTS(text=pronunciation, lang='hi')  # Change 'hi' for Hindi
        tts.save(filename)
    return filename

@app.route('/flashcards', methods=['GET'])
def flashcards():
    num_cards = request.args.get('num_cards', default=None, type=int)
    unique_labels = [key for key in letter_count if letter_count[key] != 'CHECK']

    if num_cards is not None and num_cards > 0:
        flashcards_to_display = random.sample(unique_labels, min(num_cards, len(unique_labels)))
    else:
        flashcards_to_display = unique_labels

    images = []
    pronunciations = []
    audio_files = []

    for character in flashcards_to_display:
        img_filename = f'static/images/char_{character}.png'
        images.append(img_filename)
        pronunciation = phonetic_spelling[character]
        pronunciations.append(pronunciation)

        # Generate or get the audio file for the pronunciation
        audio_filename = text_to_speech(pronunciation, letter_count[character])
        audio_files.append(audio_filename)

    return render_template('flashcards.html', 
                           letters=[letter_count[key] for key in flashcards_to_display],
                           images=images,
                           pronunciations=pronunciations,
                           audio_files=audio_files,
                           zip=zip)

@app.route('/check_pronunciation', methods=['POST'])
def check_pronunciation():
    language_code = "hi-IN"  # Use Hindi for recognition
    recognized_text = recognize_speech(language_code)  # Use your existing recognize_speech function

    # Get the character being pronounced from the request
    character_id = request.json.get('character_id')
    correct_pronunciation = phonetic_spelling[character_id]  # Get the correct pronunciation

    # Compare the recognized text with the correct pronunciation
    is_correct = recognized_text.lower() == correct_pronunciation.lower()
    
    return jsonify({'recognized_text': recognized_text, 'is_correct': is_correct})

@app.route('/say_it')
def say_it():
    character_id = random.choice(list(letter_count.keys())[1:])  # Get a random character ID
    character = letter_count[character_id]  # Get the character itself
    return render_template('say_it.html', character=character, character_id=character_id)

@app.route('/practice_mode', methods=['GET', 'POST'])
def practice_mode():
    if request.method == 'POST':
        data = request.json
        image_data = data['image']
        selected_character = data['selected_character']

        # Decode base64 image data
        image_data = image_data.split(",")[1]  # Remove the base64 header
        image = Image.open(io.BytesIO(base64.b64decode(image_data)))

        # Predict the Devanagari character drawn on the canvas
        prediction = model.predict(prepare_image(image))
        predicted_class = np.argmax(prediction[0])
        character = letter_count[predicted_class]

        # Feedback on the prediction
        feedback = 'Correct' if character == selected_character else 'Incorrect'

        return jsonify({'recognized_character': character, 'feedback': feedback})

    # Create a list of characters from the letter_count dictionary
    practice_characters = [letter for letter in letter_count.values() if letter != 'CHECK']
    selected_character = random.choice(practice_characters)
    return render_template('practice.html', 
                           practice_characters=practice_characters, 
                           selected_character=selected_character)

@app.route('/recognize/<language>', methods=['GET'])
def recognize(language):
    language_code = LANGUAGES.get(language, "en-US")
    recognized_text = recognize_speech(language_code)
    return jsonify({'recognized_text': recognized_text})

# Route to handle character recognition from a drawn image
@app.route('/recognize_character', methods=['POST'])
def recognize_character():
    image_file = request.files['image']
    image = Image.open(image_file)
    
    # Predict the Devanagari character drawn on the canvas
    prediction = model.predict(prepare_image(image))
    predicted_class = np.argmax(prediction[0])  # Get the class with the highest probability
    character = letter_count[predicted_class]
    
    return jsonify({'recognized_character': character})

# Prepare function to resize and normalize the input image for prediction
def prepare(image):
    img_array = np.array(image.convert("L"))  # Convert to grayscale
    new_array = Image.fromarray(img_array).resize((32, 32))  # Resize to 32x32 for the Devanagari model
    return np.array(new_array).reshape(-1, 32, 32, 1) / 255.0  # Normalize and reshape

# Route to handle predictions from the canvas
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    image_data = data['image'].split(",")[1]  # Extract the base64 encoded image
    image = Image.open(io.BytesIO(base64.b64decode(image_data)))  # Convert base64 to image
    
    # Prepare the image for model prediction
    prepared_image = prepare(image)
    prediction = model.predict(prepared_image)
    predicted_class = np.argmax(prediction[0])  # Get the class with the highest probability

    # Return the predicted character as a JSON response
    return jsonify({'prediction': letter_count[predicted_class]})

if __name__ == '__main__':
    app.run(debug=True)
