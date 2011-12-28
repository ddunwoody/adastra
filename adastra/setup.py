import pyglet.gl

consts = {
    'window': {
        'caption': "Ad Astra", 
        'resizable': True,
        'width': 1024,
        'height': 640,
        'config': pyglet.gl.Config(samples=8)
    },
}

def resources():
    "Adds resources to path and loads fonts"
    import pyglet.resource, pyglet.font
    pyglet.resource.path.append("@resources")
    pyglet.resource.reindex()
    pyglet.resource.add_font("PressStart2P.ttf")
    pyglet.font.load("Press Start 2P")
