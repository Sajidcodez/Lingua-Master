from tkinter import *
from tkinter import ttk
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
original_total_words = 0  # Track the total number of words


# Function to load the CSV based on selected language
def load_language_data(language):
    global to_learn, original_total_words
    try:
        # Choose the correct CSV file based on the language
        if language == "French":
            data = pd.read_csv("data/words_to_learn_french.csv")
        elif language == "Spanish":
            data = pd.read_csv("data/words_to_learn_spanish.csv")
        elif language == "Italian":
            data = pd.read_csv("data/words_to_learn_italian.csv")
    except FileNotFoundError:
        # If the "words_to_learn" file doesn't exist, load the original CSV
        if language == "French":
            original_data = pd.read_csv("data/french_words.csv")
        elif language == "Spanish":
            original_data = pd.read_csv("data/spanish_words.csv")
        elif language == "Italian":
            original_data = pd.read_csv("data/italian_words.csv")
        to_learn = original_data.to_dict(orient="records")
    else:
        to_learn = data.to_dict(orient="records")
    
    # Track the total number of words when loading data
    original_total_words = len(to_learn)
    update_progress()  # Update progress bar initially
    next_card()

# Function to load the next card
def next_card():
    global current_card, timer_flip
    window.after_cancel(timer_flip)

    # Check if there are no words left to learn
    if len(to_learn) == 0:
        canvas.itemconfig(card_title, text="Congratulations!", fill="black")
        language = selected_language.get().capitalize()
        canvas.itemconfig(card_word, text=f"All words memorized in {language}!", fill="black", font=("Times New Roman", 24, "bold"))
        canvas.itemconfig(card_background, image=card_back_img)
        # Disable the buttons when all words are memorized
        known_button.config(state="disabled")
        unknown_button.config(state="disabled")
        return  # Stop further execution

    current_card = random.choice(to_learn)
    if selected_language.get() == "French":
        canvas.itemconfig(card_title, text="French", fill="black")
        canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    elif selected_language.get() == "Spanish":
        canvas.itemconfig(card_title, text="Spanish", fill="black")
        canvas.itemconfig(card_word, text=current_card["Spanish"], fill="black")
    elif selected_language.get() == "Italian":
        canvas.itemconfig(card_title, text="Italian", fill="black")
        canvas.itemconfig(card_word, text=current_card["Italian"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    timer_flip = window.after(5000, func=flip_card)

# Function to flip the card
def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)

# Function to remove known word and update progress
def is_known():
    to_learn.remove(current_card)
    data = pd.DataFrame(to_learn)
    # Save progress in the "words_to_learn" CSV file for the selected language
    if selected_language.get() == "French":
        data.to_csv("data/words_to_learn_french.csv", index=False)
    elif selected_language.get() == "Spanish":
        data.to_csv("data/words_to_learn_spanish.csv", index=False)
    elif selected_language.get() == "Italian":
        data.to_csv("data/words_to_learn_italian.csv", index=False)
    
    update_progress()  # Update the progress bar after marking a word as known
    next_card()

# Function to update the progress bar
def update_progress():
    total_words_left = len(to_learn)
    learned_words = original_total_words - total_words_left
    if original_total_words > 0:
        progress_percent = (learned_words / original_total_words) * 100
        progress_bar['value'] = progress_percent
    else:
        progress_bar['value'] = 0

# Set up the UI
window = Tk()
window.title("Flashcard App 4 French, Spanish and Italian")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
timer_flip = window.after(5000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=1, column=0, columnspan=2)

# Progress bar setup
progress_bar = ttk.Progressbar(window, length=300, mode='determinate')
progress_bar.grid(row=3, column=0, columnspan=2)

# Buttons for right and wrong
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=2, column=0)

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=2, column=1)

# Dropdown for selecting language
selected_language = StringVar(window)
selected_language.set("French")  # Default selection
language_menu = OptionMenu(window, selected_language, "French", "Spanish", "Italian", command=load_language_data)
language_menu.grid(row=0, column=0, columnspan=2)

# Start the first flashcard with the default language
load_language_data("French")

window.mainloop()
