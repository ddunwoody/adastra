import pyglet

class AdAstraWindow(pyglet.window.Window):
    def __init__(self):
        pyglet.window.Window.__init__(self, fullscreen=True,
                                      caption="Ad Astra")
        self.set_mouse_visible(False)
        self.label = pyglet.text.Label('Hello, world',
                                       font_name='Times New Roman',
                                       font_size=36,
                                       x=self.width//2, y=self.height//2,
                                       anchor_x='center', anchor_y='center')

    def on_draw(self):
        self.clear()
        self.label.draw()

def main():
    window = AdAstraWindow()
    pyglet.app.run()

if __name__ == "__main__":
    main()
