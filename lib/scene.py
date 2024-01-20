class Scene:

    def __init__(self):
        self.layers = [[],[],[],[],[],[],[]] # 4 background layers [0, 1, 2, 3] | player layer [4] | foreground layer [5] | ui layer [6]

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

    def find(self, obj):
        for layer in self.layers:
            for o in layer:
                if o == obj:
                    return True
        return False