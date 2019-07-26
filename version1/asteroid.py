import pyglet
from random import randint
import math
from math import sin, cos, radians

win = pyglet.window.Window()
main_batch = pyglet.graphics.Batch()

pyglet.resource.path = ['/home/amalthea/hdd/PycharmProjects/asteroids/version1/resources']
pyglet.resource.reindex()

player_image = pyglet.resource.image("pixelship.png")
bullet_image = pyglet.resource.image("laser.png")
asteroid_image = pyglet.resource.image("ast1.png")

player_ship = pyglet.sprite.Sprite(img=player_image, x=400, y=300)

score_label = pyglet.text.Label(text="Score: 0", x=win.width * .9, y=win.height * .95, anchor_x='right', batch=main_batch)
level_label = pyglet.text.Label(text="Level 1", x=win.width * .5, y=win.height * .1, anchor_x='center')

asteroidImage = pyglet.resource.image('ast1.png')
asteroidSmallImage = pyglet.resource.image('ast2.png')


game_objects = []

class PhysicalObject(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(PhysicalObject, self).__init__(*args, **kwargs)
        self.vector_direction = 0
        self.vector_magnitude = 0
        self.vector_rotation = 0
        game_objects.append(self)

    def tick(self):
        self.update(
            (self.x + sin(radians(self.vector_direction)) * (self.vector_magnitude / 12)) % win.width,
            (self.y + cos(radians(self.vector_direction)) * (self.vector_magnitude / 12)) % win.height,
            self.rotation + self.vector_rotation / 12
        )

    def delete(self):
        super(PhysicalObject, self).delete()
        game_objects.remove(self)


class Asteroid(PhysicalObject):
    def __init__(self, size=0):
        super(Asteroid, self).__init__(asteroidSmallImage if size == 0 else asteroidImage,
                                       randint(0, 640),
                                       randint(0, 480)
                                       )
        self.rotation = randint(0, 360)
        direction = randint(0, 360)
        speed = randint(0, 10)


asteroids = [Asteroid(randint(0, 2)) for i in range(3)]

game_objects = [player_ship] + asteroids

player_ship = PhysicalObject(img=player_image, x=400, y=300)



def player_lives(num_icons, batch=None):
    playerlives = []
    for i in range(num_icons):
        new_sprite = pyglet.sprite.Sprite(img=player_image,
                                          x=win.width * .9 - i * 30, y=win.height * .9)
        new_sprite.scale = 0.5
        playerlives.append(new_sprite)
    return playerlives









def tick(dt):
    for po in game_objects:

        po.tick()


pyglet.clock.schedule_interval(tick, 1/120.0)

def distance(point_1=(0, 0), point_2=(0, 0)):
    """Returns the distance between two points"""
    return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


center_image(player_image)
center_image(bullet_image)
center_image(asteroid_image)

def update(dt):
    for obj in game_objects:
        obj.update(dt)

@win.event
def on_draw():
    win.clear()
    player_ship.draw()
    level_label.draw()
    score_label.draw()
    for lives in player_lives(5):
        lives.draw()
    for asteroid in asteroids:
        asteroid.draw()


if __name__ == '__main__':
    pyglet.app.run()
