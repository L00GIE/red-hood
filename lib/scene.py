class Scene:

    def __init__(self):
        self.layers = [[],[],[],[],[]]

    def loop(self):
        for layer in self.layers:
            for obj in layer:
                if hasattr(obj, "loop"):
                    obj.loop()

    def add(self, obj, layer=4):
        self.layers[layer].append(obj)

    def remove(self, obj):
        for layer in self.layers:
            if obj in layer:
                layer.remove(obj)