class Rock:
    def __init__(self,x_position, y_position,velocity, size, life):
        self.x_position = x_position
        self.y_position = y_position
        self.velocity = velocity
        self.size = size
        self.life = life 

    def move(self):
        self.x_position -= self.velocity
    
    def hitten(self, Boolean):
        if Boolean:
            self.life -= 1 