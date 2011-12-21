import cocos

class AdAstra(cocos.layer.Layer):
    def __init__(self):
        super(AdAstra, self).__init__()

        label = cocos.text.Label('Hello, Stars!',
            font_name='Times New Roman',
            font_size=32,
            anchor_x='center', anchor_y='center')

        label.position = 320, 240
        self.add(label)

if __name__ == "__main__":
    cocos.director.director.init()
    cocos.director.director.run(cocos.scene.Scene(cocos.scene.Scene(AdAstra())))
