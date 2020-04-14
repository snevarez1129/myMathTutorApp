from PIL import Image, ImageTk
import tkinter as tk

HEIGHT = 400
WIDTH = 600

def chatbot():
	print("chatbot!")

root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

myImage = Image.open("background.jpg")
background = ImageTk.PhotoImage(myImage)
background_label = tk.Label(root, image=background)
background_label.place(relwidth=1, relheight=1)

myFrame = tk.Frame(root, bg="red", bd=5)
myFrame.place(relx=0.5, rely=0.1, relwidth=0.7, relheight=0.1, anchor='n')

label = tk.Label(myFrame, text="To begin, click the button below", bg="white")
label.place(relx=0, rely=0, relwidth=1, relheight=1)

frame = tk.Frame(root, bg="red", bd=5)
frame.place(relx=0.5, rely=0.8, relwidth=0.3, relheight=0.1, anchor='n')

button = tk.Button(frame, text="Speak", bg="grey", command=chatbot)
button.place(relx=0, rely=0, relwidt=1, relheight=1)

root.mainloop()
