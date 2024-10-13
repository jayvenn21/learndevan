import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tkinter import *
from PIL import Image, ImageDraw

# Load the pre-trained Devanagari character model
model = load_model('devanagari.keras')

# Define the Devanagari class labels
letter_count = {0: 'CHECK', 1: '01_ka', 2: '02_kha', 3: '03_ga', 4: '04_gha', 5: '05_kna', 
                6: '06_cha', 7: '07_chha', 8: '08_ja', 9: '09_jha', 10: '10_yna', 
                11: '11_taa', 12: '12_thaa', 13: '13_daa', 14: '14_dhaa', 15: '15_adna', 
                16: '16_ta', 17: '17_tha', 18: '18_da', 19: '19_dha', 20: '20_na', 
                21: '21_pa', 22: '22_pha', 23: '23_ba', 24: '24_bha', 25: '25_ma', 
                26: '26_yaw', 27: '27_ra', 28: '28_la', 29: '29_waw', 30: '30_saw', 
                31: '31_petchiryakha', 32: '32_patalosaw', 33: '33_ha', 34: '34_chhya', 
                35: '35_tra', 36: '36_gya', 37: 'CHECK'}

# Prepare function to resize and normalize the input image for prediction
def prepare(image):
    img_array = np.array(image.convert("L"))  # Convert to grayscale
    new_array = Image.fromarray(img_array).resize((32, 32))  # Resize to 32x32 for the Devanagari model
    return np.array(new_array).reshape(-1, 32, 32, 1) / 255.0  # Normalize and reshape

# Function to reset the canvas and image
def reset():
    cv.delete("all")  # Clear the canvas
    global image1, draw  # Access global variables
    image1 = Image.new("RGB", (width, height), "black")  # Create a new blank image
    draw = ImageDraw.Draw(image1)  # Create a new drawing context

# Tkinter save function and model prediction
def save():
    filename = "image.png"
    image1.save(filename)  # Save the drawn image

    # Predict the Devanagari character drawn on the canvas
    prediction = model.predict(prepare(image1))
    predicted_class = np.argmax(prediction[0])  # Get the class with the highest probability
    print("Predicted character:", letter_count[predicted_class])
    
    reset()  # Reset the canvas after saving

# Tkinter paint function
def paint(event):
    x1, y1 = (event.x - 3), (event.y - 3)
    x2, y2 = (event.x + 3), (event.y + 3)
    cv.create_rectangle(x1, y1, x2, y2, fill="white")
    draw.line([x1, y1, x2, y2], fill="white", width=5)

# Tkinter loop
width = 200
height = 200
root = Tk()
cv = Canvas(root, width=width, height=height, bg='black')  # Canvas background
cv.pack()

# Create a blank PIL image for drawing
image1 = Image.new("RGB", (width, height), "black")
draw = ImageDraw.Draw(image1)

cv.bind("<B1-Motion>", paint)  # Bind paint function to mouse motion
button = Button(text="save", command=save)
button.pack()
root.mainloop()
