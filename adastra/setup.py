def resources():
    "Adds resources to path and loads fonts"
    import pyglet.resource, pyglet.font
    pyglet.resource.path.append("@resources")
    pyglet.resource.reindex()
    pyglet.resource.add_font("PressStart2P.ttf")
    pyglet.font.load("Press Start 2P")
