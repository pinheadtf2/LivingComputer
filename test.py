import random
import tkinter as tk
from PIL import ImageTk, Image
import os

class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Vivian")
        self.state('zoomed')

class ImageAnimator:
    def __init__(self, window):
        self.window = window
        self.canvas = tk.Canvas(self.window, bg="#FA8072")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.window.bind("<Configure>", self.update_canvas_size)
        self.total_time = 0

        # Load images and set durations
        self.images = [
            {"image": ImageTk.PhotoImage(Image.open("images/VivianNeutral.png")), "duration": (500, 5000)},
            {"image": ImageTk.PhotoImage(Image.open("images/VivianBlink.png")), "duration": 200}
        ]

        # Initialize current image index
        self.current_image_index = 0

        # Start the animation
        self.animate()

    def animate(self):
        # Clear the canvas
        self.canvas.delete("all")

        # Set next image var
        next_image = self.images[self.current_image_index]["image"]

        # Resize the image to fit the canvas
        resized_image = self.resize_image(ImageTk.getimage(next_image))

        # Get canvas dimensions
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # Calculate the position to center the image
        x_position = (width / 2) - (resized_image.width() / 2)
        y_position = (height / 2) - (resized_image.height() / 2)

        # Draw the current image
        self.canvas.create_image(x_position, y_position, image=resized_image, anchor="nw")

        # handle next frame time
        duration = self.images[self.current_image_index]["duration"]
        if isinstance(duration, tuple):
            remaining_time = random.randint(duration[0], duration[1]) - self.total_time
        else:
            remaining_time = duration - self.total_time

        # Update current image index
        self.current_image_index = (self.current_image_index + 1) % len(self.images)

        # Schedule next frame
        self.window.after(int(remaining_time), self.animate)

    def resize_image(self, image):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # Calculate aspect ratio
        canvas_ratio = min(width / height, height / width)
        image_ratio = image.width / image.height

        # Determine whether to scale width or height
        if image_ratio > canvas_ratio:
            new_width = int(height * image_ratio)
            new_height = height
        else:
            new_width = width
            new_height = int(width / image_ratio)

        # Resize the image
        resized_image = ImageTk.PhotoImage(image.resize((new_width, new_height)))

        return resized_image

    def update_canvas_size(self, event):
        width = event.width
        height = event.height
        print(width, height)
        self.canvas.config(width=width, height=height)

def main():
    root = Window()
    animator = ImageAnimator(root)
    root.mainloop()

if __name__ == '__main__':
    main()
