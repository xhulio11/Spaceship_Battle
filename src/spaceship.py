from pygame.constants import CONTROLLERAXISMOTION


LIFE = 10 # Life of the spaceship
W_W = 1500 # Window Width
W_H = 800 # Window height

class Spaceship:
    def __init__(self, x_position, y_position,velocity,controlls, shot):
        self.x_position = x_position
        self.y_position = y_position
        self.velocity = velocity
        self.life = LIFE
        self.shot = shot
        self.bullets = list()
        self.max_bullets = 10 
        
        """This is a list (controlls) with the kyes that will controll the spaceship
            First position -> Upwards movement
            Second position -> Downwards movement
            Third position -> Right movement
            Fourth position -> Left movement
        """    
        self.controlls = controlls 

    def move(self,pressed_key):
        # Move UP
        if pressed_key[self.controlls[0]] and self.y_position > 0:
            self.y_position -= self.velocity
        # Move DOWN
        if pressed_key[self.controlls[1]] and self.y_position < W_H - 60 :
            self.y_position += self.velocity
        # Move LEFT
        if pressed_key[self.controlls[2]] and self.x_position > 0:
            self.x_position -= self.velocity
        # Move RIGHT
        if pressed_key[self.controlls[3]] and self.x_position < W_W - 70:
            self.x_position += self.velocity
    
    # hit is a boolean
    def health(self,hit):
        if hit:
            self.life -= 1
        else:
            self.life += 1

    def remaining_bullets(self, bullet):
        if len(self.bullets)< self.max_bullets:
            self.bullets.append(bullet)


        
    
