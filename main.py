import PIL.Image
from PIL import ImageDraw, ImageFont
from tkinter import *
from tkinter import filedialog, messagebox
import os

filenames = ()
files_selected = False


# Function for opening the
# file explorer window
def browseFiles():
    global filenames, files_selected

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
            files_selected = True


def process():
    global filenames, files_selected

    if files_selected:
        # Create new img file name by continuing from the last img number
        file_name_list = os.listdir("Watermarked image")
        file_number_list = []
        char_temp = ""
        for name in file_name_list:
            for char in name:
                if char.isdigit():
                    char_temp += char
            file_number_list.append(int(char_temp))
            char_temp = ""
        try:
            maximum_number = max(file_number_list)
        except ValueError:
            maximum_number = 0

        for item in filenames:
            # get an image and convert to RGBA
            with PIL.Image.open(item).convert("RGBA") as base:
                # make a blank image for the text, initialized to transparent text color
                watermark_text_image = PIL.Image.new("RGBA", base.size, (255, 255, 255, 0))

                # get a drawing context
                draw = ImageDraw.Draw(watermark_text_image)

                # ("font type",font size)
                w, h = base.size
                x, y = int(w / 2), int(h / 2)
                if x > y:
                    font_size = y  # make text size equal to y if image is horizontal square
                else:
                    font_size = x  # make text size equal to x if image is vertical square

                # get a font
                font = ImageFont.truetype("arial.ttf", size=int(font_size / 3))

                # draw text, half opacity
                draw.text((x, y), "Water.img", font=font, fill=(64, 64, 64, 128), anchor="mb")

                # place watermark text image on top of the base image
                watermark_image = PIL.Image.alpha_composite(base, watermark_text_image)

                maximum_number += 1
                watermark_image.save(f"Watermarked image/img-{maximum_number}.png")

        text = label_file_explorer.cget("text")

        # 1 if button delete input image is On, otherwise 0.
        if checked_state.get() == 1 and text != "No image selected":
            for item in filenames:
                os.remove(item)

        label_file_explorer.configure(text="No image selected",
                                      font=("Arial", 12, "bold"),
                                      fg="red")
        messagebox.showinfo(title="Message", message="DONE!")
        files_selected = False
    else:
        messagebox.showwarning(title="Warning", message="Please select images")


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
