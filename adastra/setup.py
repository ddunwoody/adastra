def resources():
    "Adds resources to path and loads fonts"
    import pyglet.resource, pyglet.font
    pyglet.resource.path.append("@resources")
    pyglet.resource.reindex()
    pyglet.font.load("Press Start 2P")
