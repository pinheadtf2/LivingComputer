import random
import tkinter as tk
import asyncio

from playsound import playsound
from PIL import ImageTk, Image


class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.minsize(400, 200)
        self.state('zoomed')
        self.configure(bg='#FA8072')


class Frame:
    def __init__(self, image_path: str, duration: int | tuple[int, int]):
        self.image_path = image_path
        self.duration = duration

    def get_image_stats(self):
        with Image.open(self.image_path) as image:
            width, height = image.size
            return width, height

    def resize(self, target_width: int):
        with Image.open(self.image_path) as original_image:
            width, height = self.get_image_stats()
            aspect_ratio = width / height
            resized_image = original_image.resize((target_width, int(target_width / aspect_ratio)))
            # print(f"Resized image: {resized_image.width}, {resized_image.height}")
            return resized_image


class Entity:
    def __init__(self, window):
        # tkinter stuff
        self.window = window
        self.canvas = tk.Canvas(self.window, bg="#FA8072", highlightthickness=0, relief='ridge')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.window.bind("<Configure>", self.update_canvas_size)
        self.rescale = None
        self.label = None
        self.animation = None
        self.animation_sets = {}
        self.selected_set_name = None
        self.current_frame = None
        self.total_time = 0
        self.frame_index = 0

        # customizable variables, times are in millis
        self.padding_percent = 10
        self.paused_wait_period = 25
        self.resize_delay = 150
        self.text_box_padding = 100

    def rescaling_check(self, width: int, height: int):
        current_width = self.window.winfo_width()
        current_height = self.window.winfo_height()

        if (width == current_width and height == current_height and
                self.current_frame is not None):
            self.draw_frame(self.current_frame)
            self.rescale = None
        else:
            self.rescale = self.window.after(250, self.rescaling_check, current_width, current_height)

    def update_canvas_size(self, event):
        # canvas stuff
        width = event.width
        height = event.height

        # double checking if it was actually resized or not
        if width == self.canvas.winfo_width() and height == self.canvas.winfo_height():
            return
        self.canvas.config(width=width, height=height)

        # rescaling currently drawn frame if a redraw hasnt been fired yet
        if self.current_frame is not None and self.rescale is None:
            # edge case
            if width == 1 or height == 1:
                return
            self.rescale = self.window.after(250, self.rescaling_check, width, height)

    def position_image(self, image: Frame):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        padding = int(self.padding_percent * width / 100)
        resized_image = image.resize(width - padding)

        x_position = (width / 2) - (resized_image.width / 2)
        y_position = (height / 2) - (resized_image.height / 2) - (self.text_box_padding / 2)
        return resized_image, x_position, y_position

    def draw_frame(self, frame: Frame):
        if self.canvas.winfo_width() == 1 or self.canvas.winfo_height() == 1:
            return

        self.current_frame = frame
        resized_image, x_position, y_position = self.position_image(frame)
        self.window.current_image = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(x_position, y_position, image=self.window.current_image, anchor="nw", tag="entityimg")

    def animate(self):
        if self.selected_set_name is None:
            return

        # clear canvas
        self.canvas.delete("entityimg")
        self.current_frame = None

        # pull up the next image from the current anim set and draw it
        current_animation_set = self.animation_sets[self.selected_set_name]
        self.draw_frame(current_animation_set[self.frame_index])

        # handle next frame time
        duration = current_animation_set[self.frame_index].duration
        if isinstance(duration, tuple):
            remaining_time = random.randint(duration[0], duration[1]) - self.total_time
        else:
            remaining_time = duration - self.total_time

        # prep the next frame index
        self.frame_index = (self.frame_index + 1) % len(self.animation_sets[self.selected_set_name])

        # Schedule next frame
        self.animation = self.window.after(int(remaining_time), self.animate)

    def change_animation_set(self, name: str):
        if name == self.selected_set_name:
            print("AnimationSet: Not changing animation set")
            return

        if name in self.animation_sets:
            if self.animation:
                self.window.after_cancel(self.animation)
                self.animation = None
                self.current_frame = None
                self.total_time = 0
                self.frame_index = 0

            self.selected_set_name = name

    def display_text(self, text: str, counter=1):
        l.config(text=text[:counter])
        if counter < len(text):
            root.after(150, lambda: self.display_text(text, counter + 1))

class Vivian(Entity):
    def __init__(self, window):
        super().__init__(window)
        self.window.title("Vivian")

        # animation sets
        self.animation_sets["idle"] = [
            Frame("images/VivianNeutral.png", (500, 5000)),
            Frame("images/VivianBlink.png", 200)
        ]
        self.animation_sets["talking"] = [
            Frame("images/VivianNeutral.png", (150, 200)),
            Frame("images/VivianYap.png", (150, 200))
        ]

        # behaviors relevant stuff
        self.emotion = "neutral"
        self.counter = 0
        self.funny = False

    def behavior_loop(self):
        self.counter += 1
        print(self.counter)

        if self.selected_set_name is None:
            self.change_animation_set("idle")
            self.animate()

        if self.counter >= 30:
            if self.funny:
                self.funny = False
                self.counter = 0
                self.change_animation_set("idle")
                self.animate()
            else:
                self.funny = True
                self.counter = 0
                self.change_animation_set("talking")
                self.animate()

        # forever loop
        self.window.after(250, self.behavior_loop)

    def third_test(self):
        self.selected_set_name = "idle"
        self.animate()


async def run_tk(root, interval=0.05):
    try:
        while True:
            root.update()
            await asyncio.sleep(interval)
    except tk.TclError as e:
        if "application has been destroyed" not in e.args[0]:
            raise


if __name__ == '__main__':
    root = Window()
    vivian = Vivian(root)
    root.update_idletasks()
    root.after(1, vivian.behavior_loop)
    root.mainloop()
