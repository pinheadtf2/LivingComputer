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
        self.current_image_index = 0
        self.current_image = None

        # Load images and set durations
        self.images = [
            {"image": ImageTk.PhotoImage(Image.open("images/VivianNeutral.png")), "duration": (500, 5000)},
            {"image": ImageTk.PhotoImage(Image.open("images/VivianBlink.png")), "duration": 200}
        ]
        # ImageTk.getimage(self.images[0]["image"])

        # Start the animation
        self.animate()

    def animate(self):
        # Clear the canvas
        self.canvas.delete("all")

        # Set next image var
        next_image = self.images[self.current_image_index]["image"]
        x_position, y_position = self.get_centered_image_pos(next_image)

        # Draw the current image
        self.current_image = self.canvas.create_image(x_position, y_position, image=next_image, anchor="nw")

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

    def get_centered_image_pos(self, next_image):
        # Get canvas dimensions
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # Calculate the position to center the image
        x_position = (width / 2) - (next_image.width() / 2)
        y_position = (height / 2) - (next_image.height() / 2)
        return x_position, y_position

    def update_canvas_size(self, event):
        width = event.width
        height = event.height
        print(width, height)
        self.canvas.config(width=width, height=height)
        x_position, y_position = self.get_centered_image_pos(self.images[self.current_image_index]["image"])
        self.canvas.moveto(self.current_image, x_position, y_position)


def main():
    root = Window()
    animator = ImageAnimator(root)
    root.mainloop()


if __name__ == '__main__':
    main()
