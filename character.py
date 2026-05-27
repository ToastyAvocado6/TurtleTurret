import math

class PlayerTurtle:
    def __init__(self, center_x, center_y):
        self.x = center_x
        self.y = center_y
        self.hearts = 5
        self.angle = 0
        self.image = 'turtle'

    def aim_at_mouse(self, mouse_position):
        mx, my = mouse_position
        
        run = mx - self.x #horizontal and vertical distance from turtle
        rise = my - self.y
        
        radians = math.atan2(rise, run) #use some maths to calculate angle the turtle should rotate
        self.angle = math.degrees(radians)