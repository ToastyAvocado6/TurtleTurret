import math

class MovingObject:
    def __init__(self, start_x, start_y, target_x, target_y, speed, image_name):
        self.x = start_x
        self.y = start_y
        self.speed = speed
        self.image = image_name  # The string name of the image asset

        run = target_x - start_x
        rise = target_y - start_y
        distance = math.sqrt(run**2 + rise**2)

        if distance > 0:
            self.dx = (run / distance) * self.speed
            self.dy = (rise / distance) * self.speed
        else:
            self.dx = 0
            self.dy = 0

    def update_position(self):
        # Every frame, add the step vector to move the object
        self.x += self.dx
        self.y += self.dy


class PlasticBottle(MovingObject):
    def __init__(self, start_x, start_y, target_x, target_y):
        super().__init__(start_x, start_y, target_x, target_y, 2, 'plastic')

class Lettuce(MovingObject):
    def __init__(self, start_x, start_y, target_x, target_y):
        super().__init__(start_x, start_y, target_x, target_y, 3, 'lettuce')

class Bubble(MovingObject):
    def __init__(self, start_x, start_y, mouse_x, mouse_y):
        super().__init__(start_x, start_y, mouse_x, mouse_y, 8, 'bubble')