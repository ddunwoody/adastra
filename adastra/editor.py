from cocos import layer, scene
from pyglet.window import mouse, Window

from cocos.director import director
import setup

from pyglet.gl import glPushMatrix, glPopMatrix, GL_LINE_STRIP, glColor3f
from pyglet import graphics
from pyglet.window import key

from yaml import dump, load

class EditLayer(layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(EditLayer, self).__init__()
        self.polys = []
        self.current_poly = None
        self.mouse_pos = None

    def on_mouse_press(self, x, y, button, modifiers):
        x,y = director.get_virtual_coordinates(x,y)
        if button == mouse.LEFT:
            if not self.current_poly:
                self.current_poly = [x,y]
            else:
                self.current_poly.append(x)
                self.current_poly.append(y)
        if button == mouse.RIGHT:
            if self.current_poly is not None:
                self.polys.append(self.current_poly)
                self.current_poly = None

    def on_mouse_motion (self, x, y, dx, dy):
        x,y = director.get_virtual_coordinates(x,y)
        self.mouse_pos = x,y 

    def on_key_press(self, symbol, modifiers):
        if symbol == key.S:
            print "Saving polys..."
            with open("polys.yaml", "w") as f:
                dump(self.polys, f)
            print "Save complete"
        if symbol == key.L:
            print "Loading polys..."
            with open("polys.yaml", "r") as f:
                self.polys = load(f)
            print "Load complete"
        if symbol == key.C:
            if self.current_poly is not None:
                self.current_poly = None
            else:
                if (len(self.polys) > 0):
                    del self.polys[-1]

    def draw(self):
        glPushMatrix()
        self.transform()
        glColor3f(1,1,1)
        for poly in self.polys:
            graphics.draw(len(poly)/2, GL_LINE_STRIP, ("v2f", poly))
        if self.current_poly is not None:
            glColor3f(1,1,0)
            graphics.draw(len(self.current_poly)/2, GL_LINE_STRIP, ("v2f", self.current_poly))
            glColor3f(1,0,1)
            graphics.draw(2, GL_LINE_STRIP, ("v2f", (self.current_poly[-2], self.current_poly[-1], self.mouse_pos[0], self.mouse_pos[1])))
        glPopMatrix()

def main():
    setup.resources()
    director.init(**setup.consts["window"])
    director.window.set_mouse_cursor(director.window.get_system_mouse_cursor(Window.CURSOR_CROSSHAIR))
    director.run(scene.Scene(EditLayer()))


if __name__ == "__main__":
    main()
