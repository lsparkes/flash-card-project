BACKGROUND_COLOR = "#B1DDC6"
from tkinter import *
from pathlib import Path
import pandas as pd
import random

file_path = Path('./data/french_words_to_learn.csv')
fallback_path = Path('./data/french_words.csv')

try:
    data = pd.read_csv(file_path)
except FileNotFoundError:
    data = pd.read_csv(fallback_path)

to_learn_dict = data.to_dict(orient="records")
current_card = {}
flip_timer = None

def remove_learnt_words():
    global to_learn_dict, current_card
    to_learn = [word for word in to_learn_dict if word["French"] != current_card["French"]]
    df = pd.DataFrame(to_learn)
    df.to_csv("./data/french_words_to_learn.csv", index=False)
    next_card()


def next_card():
    global current_card,flip_timer

    if flip_timer is not None:
        window.after_cancel(flip_timer)

    current_card = random.choice(to_learn_dict)
    new_word = current_card["French"]
    card_canvas.itemconfig(card_title, text="French", fill="black")
    card_canvas.itemconfig(card_word, text=f"{new_word}", fill="black")
    card_canvas.itemconfig(card_image, image=card_front_img)
    flip_timer = window.after(3000, back_card)

def back_card():
    global current_card
    new_word = current_card["English"]
    card_canvas.itemconfig(card_title, text="English", fill="white")
    card_canvas.itemconfig(card_word, text=f"{new_word}", fill="white")
    card_canvas.itemconfig(card_image, image=card_back_img)

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")

card_canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_image = card_canvas.create_image(400, 263, image=card_front_img)
card_title = card_canvas.create_text(400, 150, text="Title", font=("Arial", 40, "italic"), fill="black")
card_word = card_canvas.create_text(400, 263, text="word", font=("Arial", 60, "bold"), fill="black")
card_canvas.grid(row=0, column=0, columnspan=2)

wrong_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, borderwidth=0, command=next_card)
wrong_button.grid(row=1, column=0)

right_img = PhotoImage(file="./images/right.png")
right_button = Button(image=right_img, highlightthickness=0, borderwidth=0, command=remove_learnt_words)
right_button.grid(row=1, column=1)

next_card()

window.mainloop()

