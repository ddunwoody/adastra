import pyglet
# Disable error checking for increased performance
pyglet.options['debug_gl'] = False
from pyglet.gl import *
from pyglet.window import key, mouse
from pyglet import graphics

from cocos import layer, scene, text
from cocos.director import director

from functools import wraps
import yaml

import setup

def apply_transform(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        glPushMatrix()
        self.transform()
        f(*args, **kwargs)
        glPopMatrix()
        

class EditType(object):
    LANDSCAPE = "landscape"
    SPAWN = "spawn point"


class EditMode(object):
    ADD = "adding"
    DELETE = "deleting"
    MOVE = "moving"


class Level(object):
    def __init__(self):
        self.name = None
        self.polys = []
        self.ship_spawn_pos = None


class LevelLayer(layer.Layer):
    "Draws landscape polys and ship spawn"
    def __init__(self, editor):
        super(LevelLayer, self).__init__()
        self.editor = editor

    def draw(self):
        if self.editor.level:
            glColor3f(1,1,1)
            for poly in self.editor.level.polys:
                graphics.draw(len(poly)/2, GL_LINE_LOOP, ("v2f", poly))


class StatusLayer(layer.Layer):
    "Draws status text"
    def __init__(self, editor):
        super(StatusLayer, self).__init__()
        self.editor = editor
        x,y = director.get_window_size()
        self.title = text.Label(anchor_y="top", position=(0, y))
        self.message = text.Label(anchor_y="bottom")
        self.mode = text.Label(anchor_x="right", anchor_y="bottom", halign="right", position=(x,0))
        self.add(self.title)
        self.add(self.message)
        self.add(self.mode)
        self.schedule(self.update)
        
    def update(self, dt):
        self.mode.element.text = "%s %s" % (self.editor.edit_mode, self.editor.edit_type)
        self.message.element.text = self.editor.message
    
consts = {
    'bindings': {
        },
    }    
    
class Editor(object):
    def __init__(self):
        self.edit_type = EditType.LANDSCAPE
        self.edit_mode = EditMode.ADD
        self.level = Level()
        self.message = "Ready"


class EditLayer(layer.Layer):
    is_event_handler = True

    def __init__(self, editor):
        super(EditLayer, self).__init__()
        self.editor = editor
        self.poly = None
        self.mouse_pos = None

    def on_mouse_press(self, x, y, button, modifiers):
        x,y = director.get_virtual_coordinates(x,y)
        if self.editor.edit_mode == EditMode.ADD:
            if button == mouse.LEFT:
                if self.poly:
                    map(self.poly.append, (x, y))
                    self.editor.message = "Added point at %s,%s to polygon" % (x,y)
                else:
                    self.poly = [x,y]
                    self.editor.message = "Started new polygon at %s,%s" % (x,y)
            if button == mouse.RIGHT:
                if self.poly:
                    self.editor.level.polys.append(self.poly)
                    self.poly = None
                    self.editor.message = "Added polygon to level"
                
                    
    def on_mouse_motion (self, x, y, dx, dy):
        x,y = director.get_virtual_coordinates(x,y)
        self.mouse_pos = x,y 

    def on_key_press(self, symbol, modifiers):
        if symbol == key._1:
            self.editor.edit_type = EditType.LANDSCAPE
        if symbol == key._2:
            self.editor.edit_type = EditType.SPAWN
        if symbol == key.A:
            self.editor.edit_mode = EditMode.ADD
        if symbol == key.D:
            self.editor.edit_mode = EditMode.DELETE
        if symbol == key.M:
            self.editor.edit_mode = EditMode.MOVE
#        if symbol == key.S:
#            self.set_status_line("Saving polys...")
#            with open("polys.yaml", "w") as f:
#                yaml.dump(self.polys, f)
#            self.set_status_line("Save complete")
#        if symbol == key.L:
#            self.set_status_line("Loading polys...")
#            with open("polys.yaml", "r") as f:
#                self.polys = yaml.load(f)
#            self.set_status_line("Load complete")
#        if symbol == key.C:
#            if self.current_poly is not None:
#                self.current_poly = None
#                self.set_status_line("Cancelled")
#            else:
#                if (len(self.polys) > 0):
#                    self.set_status_line("Deleted")
#                    del self.polys[-1]
#                else:
#                    self.set_status_line("No polys to delete")

#    @apply_transform
    def draw(self):
        if self.poly:
            glColor3f(1,1,0)
            graphics.draw(len(self.poly)/2, GL_LINE_STRIP, ("v2f", self.poly))
            glColor3f(1,0,1)
            graphics.draw(2, GL_LINE_STRIP, ("v2f", (self.poly[-2], self.poly[-1], self.mouse_pos[0], self.mouse_pos[1])))
            if (len(self.poly) /2 > 1):
                glColor3f(0.25,0,0)
                graphics.draw(2, GL_LINE_STRIP, ("v2f", (self.poly[-2], self.poly[-1], self.poly[0], self.poly[1])))
                glColor3f(1,0,0)
                graphics.draw(2, GL_LINE_STRIP, ("v2f", (self.mouse_pos[0], self.mouse_pos[1], self.poly[0], self.poly[1])))


def main():
    setup.resources()
    director.init(**setup.consts["window"])
    director.window.set_mouse_cursor(director.window.get_system_mouse_cursor(pyglet.window.Window.CURSOR_CROSSHAIR))

    editor = Editor()
    level_layer = LevelLayer(editor)
    status_layer = StatusLayer(editor)
    edit_layer = EditLayer(editor)
    
    director.run(scene.Scene(level_layer, status_layer, edit_layer))


if __name__ == "__main__":
    main()
