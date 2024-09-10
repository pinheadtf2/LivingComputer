import pyglet


class Vivian(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        config = pyglet.gl.Config(sample_buffers=1, samples=4, double_buffer=True)
        super().__init__(config=config, *args, **kwargs)
        self.resizable = True
        self.set_minimum_size(400, 200)
        self.set_size(1280, 720)
        pyglet.gl.glClearColor(0.98, 0.5, 0.45, 1)

        # variables
        self.padding_percent = 10

        self.image = pyglet.image.load("images/VivianNeutral.png")
        self.vivian = pyglet.sprite.Sprite(img=self.image)
        self.vivian.scale = min(self.width / self.vivian.width, self.height / self.vivian.height)

    def on_resize(self, width, height):
        # Call the parent class's on_resize method
        super().on_resize(width, height)
        print(f"Window resized to {width}x{height}")

    def on_draw(self):
        self.clear()
        self.vivian.draw()


if __name__ == '__main__':
    window = Vivian()
    pyglet.app.run()
