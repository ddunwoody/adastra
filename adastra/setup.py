def resources():
    import pyglet.resource, pyglet.font
    pyglet.resource.path.append("@adastra.resources")
    pyglet.resource.reindex()
    pyglet.resource.add_font("PressStart2P.ttf")
    pyglet.font.load("Press Start 2P")
