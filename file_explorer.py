from tkinter import *
from tkinter import filedialog, messagebox
import os

filenames = ()


# Function for opening the
# file explorer window
def browseFiles():
    global filenames

    filenames = filedialog.askopenfilenames(initialdir="/",
                                            title="Select a File",
                                            filetypes=(("All files",
                                                        "*.*"),
                                                       ("JPG file",
                                                        "*.jpg"),
                                                       ("PNG file",
                                                        "*.png"),
                                                       ))

    for item in filenames:
        if item[-3:] != "png" and item[-3:] != "jpg":
            messagebox.showerror(title="Error", message="Non-image file was selected. Please select only image file")
            label_file_explorer.configure(text="No image selected",
                                          font=("Arial", 12, "bold"),
                                          fg="red")
            browseFiles()
        else:
            # Change label contents
            label_file_explorer.configure(text=f"{len(filenames)} images have been selected ✔", fg="green")


def process():
    global filenames

    text = label_file_explorer.cget("text")

    # 1 if button delete input image is On, otherwise 0.
    if checked_state.get() == 1 and text != "No image selected":
        for item in filenames:
            os.remove(item)

    label_file_explorer.configure(text="No image selected",
                                  font=("Arial", 12, "bold"),
                                  fg="red")
    messagebox.showinfo(title="Message", message="DONE!")


# Create the root window
window = Tk()

# Set window title
window.title('Watermarker')

# Set window size
window.geometry("500x300")
window.config(pady=20)

# Create a File Explorer label
title = Label(window,
              text="Start Watermarking",
              font=("Arial", 24, "bold"),
              width=26, height=1,
              fg="black")
title.grid(column=0, row=0, pady=20)

label_file_explorer = Label(window,
                            text="No image selected",
                            font=("Arial", 12, "bold"),
                            fg="red")
label_file_explorer.grid(column=0, row=1)

button_explore = Button(window,
                        text="Browse Files",
                        font=("Arial", 12, "bold"),
                        command=browseFiles)
button_explore.grid(column=0, row=2, pady=10)

button_process = Button(window,
                        text="Process",
                        font=("Arial", 12, "bold"),
                        command=process)
button_process.grid(column=0, row=3, pady=25)

# variable to hold on to checked state, 0 is off, 1 is on.
checked_state = IntVar()
checkbutton = Checkbutton(text="Delete all input images", variable=checked_state)
checked_state.get()
checkbutton.grid(column=0, row=4, padx=20, sticky="w")

# Let the window wait for any events
window.mainloop()
