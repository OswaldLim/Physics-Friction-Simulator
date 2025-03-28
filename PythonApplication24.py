# No need to type tk before everything
import math
from matplotlib import pyplot as plt
from tkinter import *
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import customtkinter
from ttkbootstrap import Style
import webbrowser
import os


current_question = 0
score = 0

#exit button to return to mainpage after use or quit the program
def exit(window, quit='no'):
  if quit == 'yes':
    answer = messagebox.askyesno(title='Quit?',
                                 message='Are you done using the program?')
    if answer == True:
      messagebox.showinfo(title=' ', message='Thanks for using our program')
      window.destroy()
  else:
    window.destroy()
    main()


#To play the video
def play_video():
 video_url = 'https://www.youtube.com/watch?v=C8N4REG8ISE'
 webbrowser.open(video_url)


#Creates a button that when clicked it shows the theories used in our program
def theory_explanation():
  explanation_window = Tk()
  explanation_window.title('Theory Explanation')

  video_button = Button(explanation_window, text="Play Video", command=play_video, font=('Calibri, 20'))
  video_button.grid(row=1, column=0)

  canvas_2 = Canvas(explanation_window, height=750, width=1000, bg='white')
  canvas_2.grid(row=0, column=0)
  paragraph = """Newton's Second Law, 
    a cornerstone of physics, 
    reveals the connection between force, mass, and acceleration. 

    In simple terms: 
    F = ma. 
    f = m * g * μ
    Where:
    -F is the net force acting on the object,
    -m is the mass of the object, 
    -a is the acceleration produced,
    -f is the force of friction, and
    -μ is the surface friction

    Unbalanced forces lead to movement. 
    Curious? Dive deeper with our explanation video!"""
  canvas_2.create_text(500,
                         350,
                         text=paragraph,
                         justify='center',
                         font=('Calibri', 20))
  Exit_button = Button(explanation_window,
                         text='Exit',
                         font=('Calibri', 20),
                         command=lambda: exit(explanation_window))
  Exit_button.grid(row=0, column=1, pady=20)
  explanation_window.mainloop()


#functions for the quizs
def quiz_function():
  quiz = Tk()
  quiz.title("Quiz")
  # 获取当前 Python 程序文件的目录路径
  current_folder = os.path.dirname(os.path.abspath(__file__))

  # 更新quiz_data中图片路径为相对路径
  for data in quiz_data:
    # 获取图片文件名
    image_filename = os.path.basename(data["image"])
    # 构造相对路径
    relative_path = os.path.join("images", image_filename)
    # 更新字典中的路径为相对路径
    data["image"] = relative_path


  def show_question():
    global load_image
    global question
    global current_question

    if current_question >= len(quiz_data):
      current_question = 0
    question = quiz_data[current_question]
    question_label.config(text=question["question"])

    choices = question["choices"]
    option1.config(text=choices[0])
    option2.config(text=choices[1])
    option3.config(text=choices[2])
    option4.config(text=choices[3])
    print(question)
    photos = question["image"]
    load_image = Image.open(photos)
    qs_image = ImageTk.PhotoImage(load_image)

    image_label.config(image=qs_image)
    image_label.image = qs_image

  def button_click():
    check_button.config(state="disabled")

  def check():
    global score
    correct_answer = question["answer"]
    if str(radio_var.get()) == correct_answer:
        feedback_label.config(text="Your answer is correct! ", fg="green")
        score += 1
    else:
        feedback_label.config(text="Your answer is wrong! Correct answer is "+ correct_answer, fg="red")

  def next():
    global current_question
    global score
    current_question += 1

    if radio_var.get() == 0:
      messagebox.askyesno("No Answer Selected", "Please select an answer before proceeding to the next question.")
    else:
     if current_question < len(quiz_data):
        radio_var.set(0)
        check_button.config(state="normal")
        feedback_label.config(text="")
        show_question()
     else:
        messagebox.showinfo("Quiz Completed",
                            "Quiz Completed! Final score: {}/{}".format(score, len(quiz_data)))
        quiz_exit()

  def quiz_exit():
    global current_question
    if current_question < 9:
        current_question = 0
        ans=messagebox.askyesno(message='are you sure you want to exit\nYour progress will be lost.', title='Exit?')
        if ans == True:
            quiz.destroy()
    else:
        quiz.destroy()
    main()

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

  exit_button = Button(control_frame, text="Exit Quiz", command=quiz_exit)
  exit_button.grid(row=0, column=3)

  score = 0

  show_question()

  quiz.mainloop()


#to put all the graphics and input boxes onto the new window
def design_window(window):
    global canvas, box, arm, arm1

    #add temporary text to the entry box
    def add_text(event, text, textbox):
        if textbox.get() == '':
            textbox.configure(fg='white', bg='red')
            textbox.insert(0, text)

    #clear the text in the entry box
    def temp_text(event, textbox):
        textbox.configure(fg='black', bg='white')
        if textbox.get() != None:
            if not int(textbox.get()[0].isdigit()):
                textbox.delete(0, END)

    #combine add_text and temp_text to make a temporary text showing the available values in the text boxes

    #deletes leading zeroes from inputs in the input boxes
    def Change_number(event, textbox):
        leading_zero = False
        num = ''
        entry = textbox.get()
        #loops through the input and checks if there are leading zeroes
        for i in range(len(entry)):
            if leading_zero == False or leading_zero == True:
                if entry[i] == '0':
                    leading_zero = True
                    continue
                else:
                    leading_zero = 'not true'
                    num += entry[i]
                    continue
            elif leading_zero == 'not true':
                num += entry[i]
        #deletes the leading zeroes from the text box
        textbox.delete(0, END)
        textbox.insert(0, num)

    #Based on the slider value to change the surface box color.
    def update_color(surface, slider_value):
    # Map the value of the slider to the RGB range (0-255), where linear mapping is used
        color_value = int((1-(slider_value - 0.1) / (2 - 0.1)) * 155 +100)
    # Converts RGB values to hexadecimal format and formats them as Tkinter color strings
        color = "#{:02x}{:02x}{:02x}".format(color_value, color_value, color_value)
        canvas.itemconfig(surface, fill=color)

    

    # Mass input
    mass_label = customtkinter.CTkLabel(window, font = ("Arial", 20), text = "Mass:", text_color = "#16537e")
    mass_label.grid(row=0, column=0, padx = 3, pady = 3, sticky=E)

    #Doesn't use bind anymore
    mass = customtkinter.CTkEntry(window, font = ("Arial", 20), text_color = "#16537e", fg_color = "#bdd0d7", 
                                  bg_color = "#fff", border_color = "#16537e", border_width = 3, 
                                  placeholder_text = "Enter a number greater than 0", placeholder_text_color = "#fff", width = 500, height = 50)
    mass.grid(row=0, column=1, sticky=W)
    #when the user clicks off the mass input box, it adds a temporary text to the textbox allowing users to see the available
    #range of available values and also clearing the leading zeroes frominputs in the textbox

    mass.bind("<FocusOut>",
                lambda event, textbox=mass, text='Enter a number greater than 0':
                [add_text(event, text, textbox),
                Change_number(event, textbox)])



    # Applied force input

    af_label = customtkinter.CTkLabel(window, font = ("Arial", 20), text = "Applied Force:", text_color = "#16537e")
    af_label.grid(row=1, column=0, padx = 3, pady = 3, sticky=E)

    #Doesn't use bind anymore
    applied_force = customtkinter.CTkEntry(window, font = ("Arial", 20), text_color = "#16537e", 
                                           fg_color = "#bdd0d7", bg_color = "#fff", border_color = "#16537e", border_width = 3, 
                                           placeholder_text = "Enter a number greater than 0", placeholder_text_color = "#fff", width = 500, height = 50)
    applied_force.grid(row= 1, column=1, sticky=W)
    applied_force.bind(
        "<FocusOut>",
        lambda event, textbox=applied_force, text=
        'Enter a number greater than 0':
        [add_text(event, text, textbox),
        Change_number(event, textbox)])

  #turns the entry boxes red if there is no input to attract attention of users
    def reminder(event, slider):
        slider.config(bg='white')

    #initial size for the image
    coordinates = [
        int(0.1 * 150),
        int(0.1 * 150) + 20,
        int(0.1 * 150),
        int(0.1 * 150) + 20,
        int(0.1 * 150),
        int(0.1 * 150) + 20
    ]


  # to decide whether the input is valid or not
    def valid_or_not():
        Mass_str = mass.get()
        AppliedForce_str = applied_force.get()

        if Mass_str == '' or AppliedForce_str == '':
            return None
        elif Mass_str == '0':
            return None
        elif AppliedForce_str == '0':
            return None
        else:
            return 1

  #detect whether the values are positive or not
    def detect1():
        num1, num2 = Get_Values()
        if num1 is not None and num2 is not None:
            if num1 < 0:
                return None
            elif num2 < 0:
                return None
            else:
                return 1
        else:
            return None

    def call_both_methods():
        value0 = valid_or_not()
        value1 = detect1()
        if value0 == 1 and value1 == 1:
            calculate()
            push_box()
        else:
            if value0 != 1:
                text = 'Please only type in a number'
            else:
                text = 'Please type in a number'
            messagebox.showerror('Reminder', text)

  # a function to stop and put the box at the starting point
    def reset():
        global should_pause_push
        should_pause_push = False
        Distance_total = 0
        Velocity_total = 0

        global box, arm, arm1
        canvas.delete(box, arm, arm1)
        box = canvas.create_rectangle(40 + 20,
                                    415,
                                    40 + 20 + 80,
                                    415 + 60,
                                    fill="yellow")
        arm = canvas.create_rectangle(1, 435, 1 + 44, 455, fill="blue")
        arm1 = canvas.create_oval(30 + 5, 430, 30 + 30, 430 + 30, fill="white")

        global fig 
        nonlocal canvas_fig_widget
        if fig is not None:
            plt.close(fig)
            canvas.delete(canvas_fig_widget)

  # Graphics for the surfaces and animation
    canvas = Canvas(window, width=1000, height=550)
    canvas.grid(row=2, column=0, columnspan=4)

    Reset = customtkinter.CTkButton(
        master=window,
        text="Reset",
        command=reset,
        font=('Arial', 42),
        border_width=3,
        width=20,
        corner_radius=8,
        fg_color = "#327fa8",
        bg_color = "#fff",
        border_color = "#20516b",
        hover_color = "#3c487d",
        text_color = "#fff",
        hover = True)


    start = customtkinter.CTkButton(
        master=window,
        text="Push the box!",
        command=call_both_methods,
        font=('Arial', 40),
        border_width=3,
        width=20,
        corner_radius=8,
        fg_color = "#fff654",
        bg_color = "#fff",
        border_color = "#20516b",
        hover_color = "#bdd0d7",
        text_color = "#20516b",
        hover = True)

    back = customtkinter.CTkButton(
        master=window,
        text=" Back ",
        command=lambda: exit(window),
        font=('Arial', 40),
        border_width=3,
        width=20,
        corner_radius=8,
        fg_color = "#327fa8",
        bg_color = "#fff",
        border_color = "#20516b",
        hover_color = "#3c487d",
        text_color = "#fff",
        hover = True)

    button1_window = canvas.create_window(980, 10, anchor="ne", window=start)
    button2_window = canvas.create_window(980, 95, anchor="ne", window=Reset)
    button3_window = canvas.create_window(980, 185, anchor="ne", window=back)

    Surface1 = canvas.create_rectangle(60, 475, 60 + 300, 475 + 75)
    canvas.create_text(200, 510, text='Surface1')

    Surface2 = canvas.create_rectangle(360, 475, 360 + 300, 475 + 75)
    canvas.create_text(510, 510, text='Surface2')

    Surface3 = canvas.create_rectangle(660, 475, 660 + 300, 475 + 75)
    canvas.create_text(800, 510, text='Surface3')

    box = canvas.create_rectangle(40 + 20,
                                    415,
                                    40 + 20 + 80,
                                    415 + 60,
                                    fill="yellow")
    arm = canvas.create_rectangle(1, 435, 1 + 44, 455, fill="#16537e")
    arm1 = canvas.create_oval(30 + 5, 430, 30 + 30, 430 + 30, fill="#fff")


    slider_canvas = Canvas(window, width=2000, height=100)
    slider_canvas.grid(row=3, columnspan=4, pady = 5, padx = 10)

    surface_friction_label = customtkinter.CTkLabel(slider_canvas, font = ("Arial", 20), text = "  Surface Friction Sliders:  ", 
                                                    text_color = "#bdd0d7", bg_color = "#16537e")
    surface_friction_label.grid(row=0, column = 1, columnspan = 2, sticky = E)

    slider1 = Scale(slider_canvas, from_=0.1, to=2, resolution=0.01, orient=HORIZONTAL,command = lambda value:update_color(Surface1, float(value)))
    slider1.grid(row=1, column=1,padx = (200,200))
    slider2 = Scale(slider_canvas, from_=0.1, to=2, resolution=0.01, orient=HORIZONTAL,command = lambda value:update_color(Surface2, float(value)))
    slider2.grid(row=1, column=2,padx = (20,50))
    slider3 = Scale(slider_canvas, from_=0.1, to=2, resolution=0.01, orient=HORIZONTAL,command = lambda value:update_color(Surface3, float(value)))
    slider3.grid(row=1, column=3,sticky="e",padx = (150,200))


    # Get the data of Mass and AppliedForce
    def Get_Values():
        try:
            Mass_str = mass.get()
            value1 = float(Mass_str)
            AppliedForce_str = applied_force.get()
            value2 = float(AppliedForce_str)
            return value1, value2
        except ValueError:
            return None, None

  # Calculating the net force at each individual surface
    def surface(slidernum):
        Mass, AppliedForce = Get_Values()
        if int(slidernum) == 1:
            Friction_str = slider1.get()
            Friction = float(Friction_str)
        elif int(slidernum) == 2:
            Friction_str = slider2.get()
            Friction = float(Friction_str)
        else:
            Friction_str = slider3.get()
            Friction = float(Friction_str)
        Final_force = AppliedForce - (Mass) * (Friction) * 9.81
        return Final_force

  # Calculating the net force at all surfaces
  # Calculating the accelerated speed and velocity

    def calculate():
        Force1 = surface(1)
        if Force1 <= 0:
            messagebox.showerror(
                'Reminder', 'Acceleration is less than 0, change the input data.'
                '\nTry lowering the mass or the surface friction')
        Force2 = surface(2)
        Force3 = surface(3)

        print('Net force at surface 1 is: ', Force1)
        print('Net force at surface 2 is: ', Force2)
        print('Net force at surface 3 is: ', Force3)

    should_pause_push = True

    Time0 = 0.0005
    Velocities = [0]
    Times = [0]

    def push1(D0, V0):
        global should_pause_push
        Mass, AppliedForce = Get_Values()
        a = surface(1) / Mass
        while should_pause_push:
            if D0 <= 300 and V0 >= 0:
                    V_plus = a * Time0
                    V0 = V0 + V_plus
                    Shift_x = V0 * Time0
                    if V0 < 0:
                        should_pause_push = False
                        break
                    remove_object(Shift_x)
                    D0 += Shift_x
            else:
                    Time1 = 600 / V0
                    return D0, V0, Time1
                    break
        Time1 = 0
        Times.append(Time1)
        return D0, V0, Time1

    def push2(D1, V1):
        global should_pause_push
        Mass, AppliedForce = Get_Values()
        a = surface(2) / Mass
        D2 = D1
        V2 = V1
        while should_pause_push:
            if D2 <= 600 and V2 > 0:
                V_plus = a * Time0
                V2 = V2 + V_plus
                if V2 < 0:
                    should_pause_push = False
                    V2 = 0
                    Time1 = 300 / V1
                    Time2 = 2 * (D2 - 300) / (V2 + V1)
                    return D2, V2, Time2
                    break
                Shift_x = V2 * Time0
                remove_object(Shift_x)
                D2 = D2 + Shift_x
            else:
                    Time1 = 300 / V1
                    Time2 = 600 / (V2 + V1)
                    return D2, V2, Time2
                    break
        Time2 = 0
        Times.append(Time2)
        return D2, V2, Time2

    def push3(D2, V2, V1):
        global should_pause_push
        Mass, AppliedForce = Get_Values()
        a = surface(3) / Mass
        D3 = D2
        V3 = V2

        while should_pause_push:
            if D3 <= 900 and V3 > 0:
                    V_plus = a * Time0
                    V3 = V3 + V_plus
                    if V3 < 0:
                        should_pause_push = False
                        V3 = 0
                        Time1 = 300 / V1
                        Time2 = 600 / (V2 + V1)
                        Time3 = 2 * (D3 - 600) / (V2 + V3)
                        return D3, V3, Time3
                        break
                    Shift_x = V3 * Time0
                    remove_object(Shift_x)
                    D3 = D3 + Shift_x
            else:
                    Time1 = 300 / V1
                    Time2 = 600 / (V2 + V1)
                    Time3 = 600 / (V3 + V2)
                    return D3, V3, Time3
                    break
        Time3 = 0
        Times.append(Time3)
        return D3, V3, Time3

    def push_box():
        global should_pause_push, Distance_total, Velocity_total, canvas, box, arm, arm1
        Velocities = [0]
        Times = [0]
        should_pause_push = True
        Distance_total = 0
        Velocity_total = 0

        while should_pause_push:
            Distance_total_1, Velocity_total_1, t1 = push1(Distance_total,
                                                            Velocity_total)
            print(
                f" It costs {t1} on surface1,the final velocity is: {Velocity_total_1}, the distance is {Distance_total_1}"
            )
            Times.append(t1)
            Velocities.append(Velocity_total_1)

            Distance_total_2, Velocity_total_2, t2 = push2(Distance_total_1,
                                                            Velocity_total_1)
            print(
                f" It costs {t2} on surface2,the final velocity is: {Velocity_total_2}, the distance is {Distance_total_2}"
            )
            Times.append(t1 + t2)
            Velocities.append(Velocity_total_2)

            Distance_total_3, Velocity_total_3, t3 = push3(Distance_total_2,
                                                            Velocity_total_2,
                                                            Velocity_total_1)
            print(
                f" It costs {t3} on  surface3,the final velocity is: {Velocity_total_3}, the distance is {Distance_total_3}"
            )
            Times.append(t1 + t2 + t3)
            Velocities.append(Velocity_total_3)

            if Distance_total_3 >= 900:
                print(Times)
                print(Velocities)

                create_figure(Times, Velocities)
                Times.clear()
                Times = [0]
                Velocities.clear()
                Velocity_total = [0]
                should_pause_push = False

            elif Velocity_total_2 == 0 or Velocity_total_3 == 0:
                print(Times)
                print(Velocities)

                create_figure(Times, Velocities)
                print('hi')
                Times.clear()
                Times = [0]
                Velocities.clear()
                Velocity_total = [0]
                should_pause_push = False

    # function to Move the arm and the box together
    def remove_object(shift_x):
        canvas.move(box, shift_x, 0)
        canvas.move(arm, shift_x, 0)
        canvas.move(arm1, shift_x, 0)
        window.update()

    # create a original figure
    fig, ax = plt.subplots(figsize=(5, 3.8))
    ax.plot(5, 5)
    ax.set_xlabel('Time(seconds)')
    ax.set_ylabel('Velocity(meters/seconds)')
    ax.set_title('Velocity/ Time')
    canvas_fig = FigureCanvasTkAgg(fig, master=canvas)
    canvas_fig_widget = canvas.create_window(300,
                                            1,
                                            anchor='n',
                                            window=canvas_fig.get_tk_widget())
    canvas_fig.draw()

    #use the data from the experiment to draw the true figure
    def create_figure(a, b):
        global fig, clicked_points
        nonlocal canvas_fig_widget
        v_data = b
        t_data = a
        num_ticks = 10
        v_data_max = int(max(v_data))
        tick_interval = (v_data_max - 0) / num_ticks
        tick_interval = math.ceil(tick_interval)

        # Create a Matplotlib chart and determine its size
        fig, ax = plt.subplots(figsize=(5, 3.8))
        ax.plot(t_data, v_data, marker='o', markersize=5)  # Add markers here

        # Plot specific points on the line
        global specific_points
        specific_points = [(t_data[i], v_data[i]) for i in range(len(t_data))
                        if t_data[i] != 0 or v_data[i] != 0]
        for point in specific_points:
            ax.plot(point[0], point[1], marker='o', markersize=8,
                    color='black')  # black dots for specific points

        ax.set_xlabel('Time(seconds)')
        ax.set_ylabel('Velocity(meters/seconds)')
        ax.set_yticks(range(0, v_data_max, tick_interval))
        ax.set_title('Velocity/ Time')

        clicked_points = {
        }  # Dictionary to store clicked points and their annotations

         # Function to handle mouse clicks
        def on_mouse_click(event):
         global specific_points
         if event.inaxes == ax:
          for point in specific_points:
           x, y = ax.transData.transform((point[0], point[1]))
           if (x - 5 < event.x < x + 5) and (
              y - 5 < event.y < y + 5):  # Define a small area around the point
            if point not in clicked_points:  # If point is not clicked before
              time_value = round(point[0], 2)
              velocity_value = round(point[1], 2)
              annotation_text = f'(Time: {time_value} s, Velocity: {velocity_value} m/s)'
              annotation = ax.annotate(annotation_text,
                                       xy=(point[0], point[1]),
                                       xytext=(-150, -20),
                                       textcoords='offset points',
                                       arrowprops=dict(arrowstyle="->"))
              clicked_points[point] = annotation
            else:  # If point is already clicked
              annotation = clicked_points.pop(
                  point)  # Remove annotation from plot
              annotation.remove()
         fig.canvas.draw_idle()  # Update the plot with annotations

        fig.canvas.mpl_connect('button_press_event', on_mouse_click)

        canvas_fig = FigureCanvasTkAgg(fig, master=canvas)
        canvas_fig.draw()

        # Embed the chart in the Canvas and place it in the upper right corner
        canvas_fig_widget = canvas.create_window(300,
                                             1,
                                             anchor='n',
                                             window=canvas_fig.get_tk_widget())

    window.mainloop()



def create_window():
  window = customtkinter.CTk()
  window.title("Program")
  design_window(window)
  window.mainloop()


def destroy(old_window):
  old_window.destroy()


def main(window='window'):
  window = customtkinter.CTk()
  window.title("Home Page")
  window.configure(bg="#bdd0d7")
  # window.iconbitmap("")

  #Create a canvas for main window design
  main_canvas = Canvas(window, height=200, width=600, bg="#BDD0D7")
  main_canvas.grid(row=1, column=1)
  label1 = customtkinter.CTkLabel(master=main_canvas,
                                  text="FORCES",
                                  font=('Arial', 36, 'bold'),
                                  width=120,
                                  height=25,
                                  text_color="#16537e",
                                  bg_color="#fff",
                                  corner_radius=8)
  label1.place(relx=0.5, rely=0.5, anchor=CENTER)
  label2 = customtkinter.CTkLabel(
      master=main_canvas,
      text="Learn how forces can affect an object!",
      font=('Calibri', 21, 'italic'),
      width=100,
      height=20,
      corner_radius=8,
      text_color="#16537e",
      bg_color="#fff")
  label2.place(relx=0.5, rely=0.7, anchor=CENTER)

  start_button = customtkinter.CTkButton(
      master=window,
      text='Start Program',
      command=lambda: [destroy(window), create_window()],
      font=('Calibri', 25),
      border_width=3,
      width=28,
      corner_radius=8,
      fg_color="#327fa8",
      bg_color="#fff",
      border_color="#20516b",
      hover_color="#3c487d",
      text_color="#fff",
      hover=True)
  start_button.grid(row=2, column=1, padx=3, pady=5)

  theory_button = customtkinter.CTkButton(
      master=window,
      text="Learn the theory!",
      command=lambda: [destroy(window), theory_explanation()],
      font=('Calibri', 25),
      border_width=3,
      width=28,
      corner_radius=8,
      fg_color="#327fa8",
      bg_color="#fff",
      border_color="#20516b",
      hover_color="#3c487d",
      text_color="#fff",
      hover=True)
  theory_button.grid(row=3, column=1, padx=3, pady=5)

  quiz_button = customtkinter.CTkButton(
      master=window,
      text="Take Quiz",
      command=lambda: [destroy(window), quiz_function()],
      font=('Calibri', 25),
      border_width=3,
      width=28,
      corner_radius=8,
      fg_color="#327fa8",
      bg_color="#fff",
      border_color="#20516b",
      hover_color="#3c487d",
      text_color="#fff",
      hover=True)
  quiz_button.grid(row=4, column=1, padx=3, pady=5)

  exit_button = customtkinter.CTkButton(
      window,
      text='End Program',
      command=lambda: exit(window, quit='yes'),
      font=('Calibri', 25),
      border_width=3,
      width=28,
      corner_radius=8,
      fg_color="#327fa8",
      bg_color="#fff",
      border_color="#20516b",
      hover_color="#3c487d",
      text_color="#fff",
      hover=True)
  exit_button.grid(row=5, column=1, padx=3, pady=5)

  window.mainloop()

quiz_data = [
    {
        "question": """1. A wheeled cart is moving to the right at constant speed. Two forces of equal magnitude are acting upon the cart. Which of the following best describes the forces and motion of the cart?""",
        "image": "C:\\Users\\Lenovo\\Desktop\\SCHOOL\\programming and coursework\\Physics - Friction\\Fw_\\q1.png",
        "choices": ["1. Balanced Forces, Constant Speed",
                    "2. Balanced Forces, Acceleration",
                    "3. Unbalanced Forces, Constant Speed",
                    "4. Unbalanced Forces, Acceleration"],
        "answer": "1"
    },

    {
        "question": """2. How will this object move?""",
        "image": "C:\\Users\\Lenovo\\Desktop\\SCHOOL\\programming and coursework\\Physics - Friction\\Fw_\\q2.png",
        "choices": ["1. It won't move.",
                    "2. It will move to the right.",
                    "3. It will move to the left.",
                    "4. It will move up."],
        "answer": "2"
    },
    
    {
        "question": """3. How will this object move?""",
        "image": "C:\\Users\\Lenovo\\Desktop\\SCHOOL\\programming and coursework\\Physics - Friction\\Fw_\\q3.png",
        "choices": ["1. It won't move.",
                    "2. It will move to the right.",
                    "3. It will move to the left.",
                    "4. It will move in both directions."],
        "answer": "1"
    },

    {
        "question": """4. What is the net force?""",
        "image": "C:\\Users\\Lenovo\\Desktop\\SCHOOL\\programming and coursework\\Physics - Friction\\Fw_\\q4.png",
        "choices": ["1. 30 N left",
                    "2. 25 N right",
                    "3. 5 N left",
                    "4. 55 N right"],
        "answer": "3"
    },

    {
        "question": """5. What is the net force?""",
        "image": "C:\\Users\\Lenovo\\Desktop\\SCHOOL\\programming and coursework\\Physics - Friction\\Fw_\\q5.jpeg",
        "choices": ["1. 40 N left",
                    "2. 0 N balanced",
                    "3. 400 N right",
                    "4. 40 N right"],
        "answer": "4"
    },
    
    {
        "question": """6. Calculate the Net Force""",
        "image": "C:\\Users\\Lenovo\\Desktop\\SCHOOL\\programming and coursework\\Physics - Friction\\Fw_\\q6.png",
        "choices": ["1. 60N, left",
                    "2. 40N, right",
                    "3. 0N",
                    "4. 60N, right"],
        "answer": "4"
    },
        
    {
        "question": """7. Calculate the Net Force""",
        "image": "C:\\Users\\Lenovo\\Desktop\\SCHOOL\\programming and coursework\\Physics - Friction\\Fw_\\q7.png",
        "choices": ["1. 40N, left",
                    "2. 40N, right",
                    "3. 0N, balanced",
                    "4. 75N, right"],
        "answer": "3"
    },

    {
        "question": """8. What is the net force?""",
        "image": "C:\\Users\\Lenovo\\Desktop\\SCHOOL\\programming and coursework\\Physics - Friction\\Fw_\\q8.png",
        "choices": ["1. 10N",
                    "2. 0N",
                    "3. 25N",
                    "4. 1N"],
        "answer": "2"
    },

    {
        "question": """9. Forces that have a net force of zero (the object is still). """,
        "image": "C:\\Users\\Lenovo\\Desktop\\SCHOOL\\programming and coursework\\Physics - Friction\\Fw_\\q9.jpeg",
        "choices": ["1. Balanced force",
                    "2. Unbalanced force",
                    "3. NA",
                    "4. NA"],
        "answer": "1"
    },
]


main()
