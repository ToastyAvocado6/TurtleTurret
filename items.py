import math
import random

class MovingObject:
    def __init__(self, start_x, start_y, target_x, target_y, speed, image_name):
        self.x = start_x
        self.y = start_y
        self.speed = speed
        self.image = image_name  

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
        self.x += self.dx
        self.y += self.dy


class PlasticBottle(MovingObject):
    def __init__(self, start_x, start_y, target_x, target_y):
        super().__init__(start_x, start_y, target_x, target_y, 2, 'plastic')
        self.health = 2
        self.render_angle = random.randint(0, 360)

    def hit(self):
        self.health -= 1
        if self.health == 1:
            self.image = 'plastic_2' 
        return self.health <= 0


class Lettuce(MovingObject):
    def __init__(self, start_x, start_y, target_x, target_y):
        super().__init__(start_x, start_y, target_x, target_y, 3, 'lettuce')
        self.health = 1
        self.render_angle = random.randint(0, 360)

    def hit(self):
        self.health -= 1
        return self.health <= 0 


class Bubble(MovingObject):
    def __init__(self, start_x, start_y, mouse_x, mouse_y):
        super().__init__(start_x, start_y, mouse_x, mouse_y, 8, 'bubble')
        self.is_popping = False
        self.pop_frames = ['bubble', 'bubble_2', 'bubble_3', 'bubble_4']
        self.frame_index = 0.0
        self.animation_speed = 0.25

    def pop(self):
        self.is_popping = True
        self.dx = 0
        self.dy = 0
                
    def update_position(self, tracking_list):
        if not self.is_popping:
            super().update_position()
        else:
            self.frame_index += self.animation_speed
            # FIX: Cleanly drops the object from the active scene array immediately on animation wrap
            if int(self.frame_index) >= len(self.pop_frames):
                if self in tracking_list:
                    tracking_list.remove(self)
            else:
                self.image = self.pop_frames[int(self.frame_index)]