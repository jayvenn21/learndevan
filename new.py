import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv("data.csv")
dataset = np.array(data)

# Shuffle the dataset
np.random.shuffle(dataset)

# Extract features and labels
X = dataset[:, 0:1024]  # Assuming the images are in the first 1024 columns
Y = dataset[:, 1024]     # Assuming the labels are in the last column

# Function to display one sample image for each unique character
def display_single_sample_per_character(images, labels):
    unique_labels = np.unique(labels)  # Get unique character labels
    num_labels = len(unique_labels)
    
    # Create a figure with a subplot for each character
    plt.figure(figsize=(20, 5))  # Increased width for better spacing
    
    for i, character in enumerate(unique_labels):
        # Get the indices of images corresponding to the current character
        char_indices = np.where(labels == character)[0]
        
        # Select the first image found for the current character
        if len(char_indices) > 0:
            plt.subplot(1, num_labels, i + 1)
            plt.title(f'Character: {character}', fontsize=12)
            img = images[char_indices[0]].reshape(32, 32)  # Reshape to the original image size (32x32)
            plt.imshow(img, cmap='gray')  # Display the first image for this character
            plt.axis('off')  # Hide axis
            
    plt.subplots_adjust(wspace=0.5)  # Adjust the space between subplots
    plt.show()

# Display one sample for each character from the dataset
display_single_sample_per_character(X, Y)
