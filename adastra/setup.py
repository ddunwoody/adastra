def resources():
    import pyglet.resource, pyglet.font
    pyglet.resource.path.append("@adastra.resources")
    pyglet.resource.reindex()
    pyglet.resource.add_font("PressStart2P.ttf")
    pyglet.font.load("Press Start 2P")

def gl():
    from pyglet.gl import glTexParameteri, GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_NEAREST
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
