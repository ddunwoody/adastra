from cocos.cocosnode import CocosNode
from cocos.director import director

from pyglet.gl import glPushMatrix, glPopMatrix, GL_LINES, glColor3f
import pyglet.graphics


class GLNode(CocosNode):
    def __init__(self):
        super(GLNode, self).__init__()
    
    def draw(self):
        glPushMatrix()
        self.transform()
        self.drawGl()
        glPopMatrix()
        
    def drawGl(self):
        pass

    
class Ground(GLNode):
    def __init__(self, altitude):
        super(Ground, self).__init__()
        self.width = director.get_window_size()[0]
        self.altitude = altitude
    
    def drawGl(self):
        glColor3f(0,0.5,0)
        offset = 0
        x1, x2 = 0, self.width
        for i in range(8):
            y = self.altitude - offset
            pyglet.graphics.draw(2, GL_LINES, ('v2i', (x1, y, x2, y)))
            offset += i*2
    
