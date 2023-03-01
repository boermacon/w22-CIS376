import pygame

class Scene:

    updateables = []
    drawables = []
    colors = {
        "WHITE": (255, 255, 255),
        "BLACK": (0,0,0)
    }
    FPS = None

    def __init__(self):
        pass

    def update(self):
        for object in Scene.updateables:
            object.update()

    def draw(self):
        for object in Scene.drawables:
            object.draw()
        
