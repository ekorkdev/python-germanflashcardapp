from tkinter import *
from random import choice
from tkinter.font import BOLD, ITALIC
import pandas

# ---------------------------------------- RANDOM WORD ------------------------------------------------------------
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/german_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def generate_word():
    global random_word, flash_timer
    window.after_cancel(flash_timer)
    random_word = choice(to_learn)
    canvas.itemconfig(canvas_image, image=card_front)
    canvas.itemconfig(card_title, text="German", fill="black")
    canvas.itemconfig(card_word, text=random_word['German'], fill="black")
    flash_timer = window.after(3000, flash_card)

def remove_word():
    to_learn.remove(random_word)
    wdata = pandas.DataFrame(to_learn)
    wdata.to_csv("data/words_to_learn.csv", index=False)
    generate_word()

# ---------------------------------------- FLASH CARD ------------------------------------------------------------
def flash_card():
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=random_word['English'], fill="white")

# ---------------------------------------- WINDOW ------------------------------------------------------------

window = Tk()
window.title("German Flash Card App")
window.config(padx=50, pady=50, background="#B1DDC6")
flash_timer = window.after(3000, flash_card)

# ---------------------------------------- CANVAS ------------------------------------------------------------

canvas = Canvas(height=526, width=800, highlightthickness=0, background="#B1DDC6")
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, ITALIC))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, BOLD))
canvas.grid(row=0, column=0, columnspan=2)

# ---------------------------------------- BUTTONS ---------------------------------------------------------

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=remove_word)
right_button.grid(row=1, column=0)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=generate_word)
wrong_button.grid(row=1, column=1)

# ---------------------------------------- RUN ---------------------------------------------------------

generate_word()

window.mainloop()