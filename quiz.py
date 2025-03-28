from tkinter import *
from tkinter import messagebox, ttk
from tkinter.ttk import Button
from PIL import Image, ImageTk
from ttkbootstrap import Style
from quiz_data import quiz_data

quiz = Tk()
quiz.title("Quiz")

current_question = 0

def show_question():
    global load_image
    global question

    question = quiz_data[current_question]
    question_label.config(text=question["question"])

    choices = question["choices"]
    option1.config(text=choices[0])
    option2.config(text=choices[1])
    option3.config(text=choices[2])
    option4.config(text=choices[3])

    photos = question["image"]
    load_image = Image.open(photos)
    qs_image = ImageTk.PhotoImage(load_image)

    image_label.config(image=qs_image)
    image_label.image = qs_image

def button_click():
    check_button.config(state="disabled")

def check():
    correct_answer = question["answer"]
    if str(radio_var.get()) == correct_answer:
        feedback_label.config(text="Your answer is correct! ", fg="green")
        global score
        score += 1
    else:
        feedback_label.config(text="Your answer is wrong! Correct answer is "+ correct_answer, fg="red")

def next():
    global current_question
    current_question += 1

    if current_question < len(quiz_data):
        radio_var.set(0)
        check_button.config(state="normal")
        feedback_label.config(text="")
        show_question()
    else:
        messagebox.showinfo("Quiz Completed",
                            "Quiz Completed! Final score: {}/{}".format(score, len(quiz_data)))
        quiz.destroy()

def previous():
    global current_question
    current_question -= 1

    if current_question < 0:
        messagebox.showinfo("First Question",
                            "This is the first question of the quiz")
        current_question = 0
        check_button.config(state="normal")
        return
    else:
        radio_var.set(0)
        feedback_label.config(text="")
        show_question()

image_label = Label(quiz)
image_label.grid(row=0, column=0)

question_label = Label(quiz,
                       font=("Calibri", 16),
                       height=5,
                       width=50,
                       wraplength=375)
question_label.grid(row=0, column=1)

feedback_label = Label(quiz,
                       font=("Calibri", 20, "bold"))
feedback_label.grid(row=2, column=0, columnspan=3)

option_frame = Frame(quiz)
option_frame.grid(row=1, column=0)

radio_var = IntVar()
radio_var.set(0)

option1 = Radiobutton(option_frame,
                      font=("Calibri", 14),
                      variable=radio_var,
                      value=1)
option2 = Radiobutton(option_frame,
                      font=("Calibri", 14),
                      variable=radio_var,
                      value=2)
option3 = Radiobutton(option_frame,
                      font=("Calibri", 14),
                      variable=radio_var,
                      value=3)
option4 = Radiobutton(option_frame,
                      font=("Calibri", 14),
                      variable=radio_var,
                      value=4)

option1.grid(row=0, column=0)
option2.grid(row=0, column=1)
option3.grid(row=1, column=0)
option4.grid(row=1, column=1)

control_frame = Frame(quiz)
control_frame.grid(row=1, column=1)

check_button = Button(control_frame, text="Check Answer", command=lambda:[check(), button_click()])
check_button.grid(row=0, column=1)

next_button = Button(control_frame, text="Next Question", command=next)
next_button.grid(row=0, column=2)

previous_button = Button(control_frame, text="Previous Question", command=previous)
previous_button.grid(row=0, column=0)

score = 0

current_question = 0

show_question()

quiz.mainloop()
