import math

class Health_Kit():
    def __init__(self,x_position,starting_point, health, velocity):
        self.x_position = x_position
        self.y_position = starting_point
        self.starting_point = starting_point
        self.health = health
        self.velocity = velocity
        self.frequency = 0.003
    
    def move(self,):
        self.x_position -= self.velocity
        self.y_position = 200*math.sin(self.x_position*2*math.pi*self.frequency) + self.starting_point 
