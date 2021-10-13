class Bullet():
    def __init__(self,x_position, y_position, velocity):
        self.x_position = x_position
        self.y_position = y_position
        self.velocity = velocity

    
    def shot(self):
        self.x_position += self.velocity
    