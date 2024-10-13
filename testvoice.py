import tkinter as tk
import threading
import speech_recognition as sr

# Language dictionary mapping languages to Google Speech API language codes
LANGUAGES = {
    "Afrikaans": "af-ZA",
    "Amharic": "am-ET",
    "Arabic": "ar-SA",
    "Basque": "eu-ES",
    "Bulgarian": "bg-BG",
    "Catalan": "ca-ES",
    "Cantonese (Traditional)": "yue-Hant-HK",
    "Chinese (Mandarin - Simplified)": "zh-CN",
    "Chinese (Mandarin - Traditional)": "zh-TW",
    "Croatian": "hr-HR",
    "Czech": "cs-CZ",
    "Danish": "da-DK",
    "Dutch": "nl-NL",
    "English (US)": "en-US",
    "English (UK)": "en-GB",
    "Estonian": "et-EE",
    "Filipino": "fil-PH",
    "Finnish": "fi-FI",
    "French": "fr-FR",
    "German": "de-DE",
    "Greek": "el-GR",
    "Gujarati": "gu-IN",
    "Hebrew": "he-IL",
    "Hindi": "hi-IN",
    "Hungarian": "hu-HU",
    "Icelandic": "is-IS",
    "Indonesian": "id-ID",
    "Italian": "it-IT",
    "Japanese": "ja-JP",
    "Javanese": "jv-ID",
    "Kannada": "kn-IN",
    "Korean": "ko-KR",
    "Latvian": "lv-LV",
    "Lithuanian": "lt-LT",
    "Malay": "ms-MY",
    "Malayalam": "ml-IN",
    "Marathi": "mr-IN",
    "Nepali": "ne-NP",
    "Norwegian": "no-NO",
    "Persian": "fa-IR",
    "Polish": "pl-PL",
    "Portuguese (Brazil)": "pt-BR",
    "Portuguese (Portugal)": "pt-PT",
    "Punjabi": "pa-IN",
    "Romanian": "ro-RO",
    "Russian": "ru-RU",
    "Serbian": "sr-RS",
    "Slovak": "sk-SK",
    "Slovenian": "sl-SI",
    "Spanish (Spain)": "es-ES",
    "Spanish (Mexico)": "es-MX",
    "Swahili": "sw-KE",
    "Swedish": "sv-SE",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
    "Thai": "th-TH",
    "Turkish": "tr-TR",
    "Ukrainian": "uk-UA",
    "Urdu": "ur-PK",
    "Vietnamese": "vi-VN",
    "Zulu": "zu-ZA"
}

# Function to recognize speech and update text in the GUI
def recognize_speech(language_code):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            try:
                print(f"Listening in {language_code}...")
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio, language=language_code)
                print(f"Recognized: {text}")
                update_text(text)
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError:
                print("Request error from speech recognition service")
            except sr.WaitTimeoutError:
                print("Listening timed out")

# Function to update the label with recognized text
def update_text(text):
    result_label.config(text=text)

# Function to run speech recognition in a separate thread
def start_speech_recognition():
    selected_language = language_var.get()
    language_code = LANGUAGES.get(selected_language, "en-US")
    speech_thread = threading.Thread(target=recognize_speech, args=(language_code,))
    speech_thread.daemon = True  # So the thread closes when the app closes
    speech_thread.start()

# Tkinter GUI setup
root = tk.Tk()
root.title("Speech to Text Interface")

# Language selection dropdown
language_var = tk.StringVar(root)
language_var.set("English")  # Default language
language_label = tk.Label(root, text="Select Language:", font=("Helvetica", 14))
language_label.pack(pady=10)

language_menu = tk.OptionMenu(root, language_var, *LANGUAGES.keys())
language_menu.config(font=("Helvetica", 12))
language_menu.pack(pady=10)

# Result label to display the spoken text
result_label = tk.Label(root, text="Speak something...", font=("Helvetica", 20), wraplength=400)
result_label.pack(pady=20)

# Start button to begin speech recognition
start_button = tk.Button(root, text="Start Listening", command=start_speech_recognition, font=("Helvetica", 14))
start_button.pack(pady=10)

root.geometry("500x400")
root.mainloop()
