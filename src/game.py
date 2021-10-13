import pygame
from pygame.constants import KEYDOWN
from health_kit import Health_Kit
from spaceship import Spaceship
from bullet import Bullet
from rock import Rock
from random import randrange
from health_kit import Health_Kit
import random
from datetime import datetime, date
import os,json

pygame.font.init()
pygame.mixer.init()

class Game:
    def __init__(self, W_H, W_W, FPS):
        self.W_H = W_H
        self.W_W = W_W
        self.FPS = FPS
        self.BULLETS = 7
        self.Active = True # The game is running
        self.Score = 0
        self.Health = 10
        with open(os.path.join("game_files", "leader_board.json"), "r") as file:
            self.leader_board = json.load(file)

        self.LEVEL = 2        
        self.BACKGROUND_1 = None
        self.BACKGROUND_2 = None
        self.RED_SPACESHIP = None
        self.GRENADE_SOUND = None
        self.GUN_SOUND = None
        self.BULLET = None
        self.ROCK = None
        
        "Intitialzing Everything"
        pygame.init()
        self.loader() # Loading images and sounds
        pygame.display.set_caption("Spaceship Battle") # Naming the Game
        self.screen = pygame.display.set_mode((W_W,W_H)) # Creating a screen
        pygame.display.set_icon(pygame.image.load(os.path.join('Assets', 'spaceship_red.png')))
        self.clock = pygame.time.Clock()
   
    """Loading Photos and Sounds"""
    def loader(self):
        pygame.mixer.init()
        self.BACKGROUND_1 = pygame.image.load(os.path.join('Assets', 'space.png'))
        self.BACKGROUND_1 = pygame.transform.scale(self.BACKGROUND_1, (self.W_W, self.W_H))
        self.BACKGROUND_2= pygame.image.load(os.path.join('Assets', 'space.png'))
        self.BACKGROUND_2= pygame.transform.scale(self.BACKGROUND_2, (self.W_W, self.W_H))
        
        self.RED_SPACESHIP = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
        self.RED_SPACESHIP = pygame.transform.scale(self.RED_SPACESHIP,(60, 70))
        self.RED_SPACESHIP = pygame.transform.rotate(self.RED_SPACESHIP, 90)
        
        self.BULLET = pygame.image.load(os.path.join('Assets', 'bullet.png'))
        self.BULLET.set_colorkey((0, 0, 0))
        self.BULLET = pygame.transform.scale(self.BULLET,(20, 20))
        self.BULLET = pygame.transform.rotate(self.BULLET, 270)

        self.ROCK_1 = pygame.image.load(os.path.join('Assets', 'rock.png'))
        self.ROCK_1.set_colorkey((0,0,0))
        self.ROCK_1 = pygame.transform.scale(self.ROCK_1, (50,50))

        self.ROCK_2 = pygame.image.load(os.path.join('Assets', 'rock.png'))
        self.ROCK_2.set_colorkey((0,0,0))
        self.ROCK_2 = pygame.transform.scale(self.ROCK_2, (100,100))
        
        self.ROCK_3 = pygame.image.load(os.path.join('Assets', 'rock.png'))
        self.ROCK_3.set_colorkey((0,0,0))
        self.ROCK_3 = pygame.transform.scale(self.ROCK_3, (150,150))
    
        self.HEALTH_KIT = pygame.image.load(os.path.join('Assets','Health_Kit.png'))
        self.HEALTH_KIT.set_colorkey((0,0,0))
        self.HEALTH_KIT = pygame.transform.scale(self.HEALTH_KIT,(60,60))

        self.FIRE = pygame.image.load(os.path.join('Assets', 'fire.png'))
        self.FIRE.set_colorkey((0,0,0))
        self.FIRE = pygame.transform.scale(self.FIRE, (60,60))
        self.FIRE = pygame.transform.rotate(self.FIRE, 90)

        self.GRENADE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade.mp3'))
        self.GUN_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun.mp3'))
        self.LOSING_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Losing_sound.mp3'))
        self.PUNCH = pygame.mixer.Sound(os.path.join('Assets', 'Punch.mp3'))
    
    
    def running_game(self):
        self.Active = True
        random.seed(datetime.now())
        status = False # We use this variable for health-kit 
        # Variables to control moving background
        x_background_1 = 0 
        x_background_2 = self.W_W
        y_background_1 = y_background_2 = 0
        health_kit_1 = Health_Kit(self.W_W,self.W_H//2, 5, 4)
        next_level = self.LEVEL + 1
        font = pygame.font.SysFont("dejavuserif", 25)
        
        # Creating SpaceShip
        red_spaceship = Spaceship(70, 300, 7,[pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT], self.BULLETS )         
        
        # Creating Rocks
        rocks_1, rocks_2, rocks_3 = self.rock_creator()
        
        while self.Active:
            self.clock.tick(self.FPS) # Setting the Frame Rate
            # Controlling if all rocks are destroyed
            if len(rocks_1)==len(rocks_2) ==len(rocks_3) == 0:
                self.LEVEL += 1
                self.BULLETS += 1
                print("ROCKS are DESTROYED: LEVEL " + str(self.LEVEL))
                rocks_1, rocks_2, rocks_3 = self.rock_creator()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Active = False
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause(x_background_1, y_background_1, x_background_2, y_background_2,red_spaceship, rocks_1, rocks_2, rocks_3, font)
                
                # Making spaceship with 3 bullets in a certen level
                if event.type == pygame.KEYDOWN and self.LEVEL > 10:
                    if event.key == pygame.K_SPACE and len(red_spaceship.bullets) < red_spaceship.max_bullets:
                        bullet = Bullet(red_spaceship.x_position, red_spaceship.y_position + 17, 12)
                        bullet_up = Bullet(red_spaceship.x_position, red_spaceship.y_position , 12) 
                        bullet_down = Bullet(red_spaceship.x_position, red_spaceship.y_position + 34, 12)
                        red_spaceship.bullets.append(bullet)
                        red_spaceship.bullets.append(bullet_up)
                        red_spaceship.bullets.append(bullet_down)
                        pygame.mixer.Sound.play(self.GUN_SOUND)
                
                # Making spaceship with only one bullet
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and len(red_spaceship.bullets) < red_spaceship.max_bullets:
                        bullet = Bullet(red_spaceship.x_position, red_spaceship.y_position + 17, 10)
                        red_spaceship.bullets.append(bullet)
                        pygame.mixer.Sound.play(self.GUN_SOUND)
                

            pressed_keys = pygame.key.get_pressed()      
            red_spaceship.move(pressed_keys)
            self.screen.blit(self.BACKGROUND_1, (x_background_1,y_background_1))
            self.screen.blit(self.BACKGROUND_2, (x_background_2,y_background_2))
            self.screen.blit(self.RED_SPACESHIP, (red_spaceship.x_position, red_spaceship.y_position))

            """Drawing the bullets in the Screen"""
            for bullet in red_spaceship.bullets:
                bullet.shot()
                self.screen.blit(self.BULLET, (bullet.x_position, bullet.y_position))
                if bullet.x_position > self.W_W:
                    red_spaceship.bullets.remove(bullet) 

            """Drawing Rocks in the Screen"""
            for rock in rocks_1:
                self.screen.blit(self.ROCK_1, (rock.x_position, rock.y_position))
                rock.move()
            
            for rock in rocks_2:
                self.screen.blit(self.ROCK_2, (rock.x_position, rock.y_position))
                rock.move()
            
            for rock in rocks_3:
                self.screen.blit(self.ROCK_3, (rock.x_position, rock.y_position))
                rock.move()

            """Drawing Score"""
            text = font.render("Score: " + str(self.Score), True, "white")
            textRect = text.get_rect()
            textRect.center = (self.W_W//2, 40)
            self.screen.blit(text, textRect)

            """Drawing Health"""         
            health = pygame.Rect(self.W_W//2 - 100, 10, 200 , 10)
            pygame.draw.rect(self.screen, "red",health)

            health = pygame.Rect(self.W_W//2 - 100, 10, 20*self.Health , 10)
            pygame.draw.rect(self.screen, "white",health)
            
            """Drawing the Health - Kit"""
            if random.randrange(2000) == 20  or status:
                self.screen.blit(self.HEALTH_KIT, (health_kit_1.x_position, health_kit_1.y_position))
                answer= self.health_kit_control(red_spaceship, health_kit_1)
                health_kit_1.move() 
                status = True
                if answer:
                    health_kit_1.x_position = self.W_W
                    health_kit_1.y_position = self.W_H//2
                    status = False

            pygame.display.update()
            self.crash_control(red_spaceship, rocks_1, 2)
            self.crash_control(red_spaceship, rocks_2, 3)
            self.crash_control(red_spaceship, rocks_3, 4)

            # Making the moving background
            x_background_1 += -1
            x_background_2 += -1
            if x_background_1 < -self.W_W:
                x_background_1 = self.W_W
            if  x_background_2 < -self.W_W:
                x_background_2 = self.W_W
        
        # Displaying the Losing Text
        self.losing(x_background_1, x_background_2, y_background_1, y_background_2, red_spaceship, )
    

    def crash_control(self, red_spaceship, rocks, rock_type):
        
        for rock in rocks:  
            if (rock.x_position + 10 <= red_spaceship.x_position + 40 <= rock.x_position + rock.size + 10  and 
                rock.y_position - 30 < red_spaceship.y_position< rock.y_position + rock.size - 30): 
                if self.Health < 0:
                    self.Active = False
                else:
                    self.Health -= rock_type
                    rocks.remove(rock)
                    pygame.mixer.Sound.play(self.PUNCH)
                    if self.Health < 0:
                        self.Active = False
                    continue
            
            elif rock.x_position < -rock.size:
                self.Score -= rock_type 
                rocks.remove(rock)

            for bullet in red_spaceship.bullets:
                if rock.x_position < bullet.x_position < rock.x_position + 20 and  rock.y_position <= bullet.y_position <= rock.y_position + rock.size:
                    # removing the bullet from the screen and controlling the life of the hitten rock
                    pygame.mixer.Sound.play(self.GRENADE_SOUND)
                    self.screen.blit(self.FIRE, (bullet.x_position - 40, bullet.y_position - 15))
                    red_spaceship.bullets.remove(bullet)
                    rock.hitten(True)
                    if rock.life == 0:
                        rocks.remove(rock)
                        self.Score += 1
        pygame.display.update()
                
    
    def rock_creator(self):
        # Creating Rock Objects
        rocks_1 = [Rock(randrange(self.W_W,self.W_W + 1000), randrange(self.W_H - 50), 3, 50, 2) for _ in range(self.LEVEL)]
        rocks_2 = [Rock(randrange(self.W_W,self.W_W + 2000), randrange(self.W_H - 100), 3, 100, 3) for _ in range(self.LEVEL )]
        rocks_3 = [Rock(randrange(self.W_W,self.W_W + 3000), randrange(self.W_H - 150), 3, 150, 4) for _ in range(self.LEVEL)]
        
        return rocks_1, rocks_2, rocks_3


    def losing(self,x_background_1, x_background_2, y_background_1, y_background_2, red_spaceship):

        pygame.mixer.Sound.play(self.LOSING_SOUND)
        yes_button_color = "white"
        no_button_color = "white"

        font = pygame.font.SysFont("dejavuserif", 100)
        text = font.render("YOU LOSE", True, "white")
        textRect = text.get_rect()
        textRect.center = (self.W_W // 2, self.W_H// 10)
            
        font_2 = pygame.font.SysFont("dejavuserif", 40)
        text_2 = font_2.render("Would you like to store your Score?", True, "white")
        textRect_2= text_2.get_rect()
        textRect_2.center = (self.W_W //2, self.W_H// 10 + 100)
        
        yes_font = pygame.font.SysFont("dejavuserif", 40)
        

        no_font = pygame.font.SysFont("dejavuserif", 40)
        
        while True:
            # Rendering YES Button
            yes_text = yes_font.render("YES", True, yes_button_color)
            yes_Rect = yes_text.get_rect()
            yes_Rect.center = (self.W_W//2 - 100, self.W_H/10 + 200)

            # Rendering NO Button
            no_text = no_font.render("NO", True, no_button_color)
            no_Rect = no_text.get_rect()
            no_Rect.center = (self.W_W//2 + 100, self.W_H/10 + 200)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Active = False
                    pygame.quit()
                mouse = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If NO, go to main menu
                    if self.W_W//2 + 50 < mouse[0] < self.W_W//2 + 150 and self.W_H//10 + 150 < mouse[1] < self.W_H//10 + 250:
                        self.main_menu()
                    elif self.W_W//2 - 150 < mouse[0] < self.W_W//2 - 50 and self.W_H//10 + 150 < mouse[1] < self.W_H//10 + 240:
                        self.add_score()

            mouse = pygame.mouse.get_pos()
            
            # for NO Button
            if self.W_W//2 + 50 < mouse[0] < self.W_W//2 + 150 and self.W_H//10 + 150 < mouse[1] < self.W_H//10 + 240:
                no_button_color = "blue"
            else:
                no_button_color = "white" 
            # for YES Button
            if self.W_W//2 - 150 < mouse[0] < self.W_W//2 - 50 and self.W_H//10 + 150 < mouse[1] < self.W_H//10 + 240:
                yes_button_color = "blue"
            else:
                yes_button_color = "white"
            
            self.screen.blit(self.BACKGROUND_1, (x_background_1,y_background_1))
            self.screen.blit(self.BACKGROUND_2, (x_background_2,y_background_2))
            self.screen.blit(self.RED_SPACESHIP, (red_spaceship.x_position, red_spaceship.y_position))

            
            """Drawing the bullets in the Screen"""
            for bullet in red_spaceship.bullets:
                bullet.shot()
                self.screen.blit(self.BULLET, (bullet.x_position, bullet.y_position))
            
            """Displaying text element and Buttons on the screen"""
            self.screen.blit(text, textRect)
            self.screen.blit(text_2, textRect_2)
            self.screen.blit(yes_text, yes_Rect)
            self.screen.blit(no_text, no_Rect)
            pygame.display.update()


    def health_kit_control(self,spaceship, health_kit):
    
        # If spaceship touches the box, it takes health (True)
        if (health_kit.x_position < spaceship.x_position + 60 < health_kit.x_position + 60 and
            health_kit.y_position - 70 < spaceship.y_position < health_kit.y_position + 60):
            if self.Health + health_kit.health <= 10:
                self.Health += health_kit.health
            else:
                self.Health = 10
            return True 
        # If spaceship does not touch the box, it does not take something (False)
        elif health_kit.x_position < -60:
            return True


    def pause(self,x_background_1, y_background_1, x_background_2, y_background_2,red_spaceship, rocks_1, rocks_2, rocks_3, font ):
        active = True
        Pause = pygame.font.SysFont("dejavuserif", 100) 
        clock = pygame.time.Clock()
        while active:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Active = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        active = False

            self.screen.blit(self.BACKGROUND_1, (x_background_1,y_background_1))
            self.screen.blit(self.BACKGROUND_2, (x_background_2,y_background_2))
            self.screen.blit(self.RED_SPACESHIP, (red_spaceship.x_position, red_spaceship.y_position))

            """Drawing the bullets in the Screen"""
            for bullet in red_spaceship.bullets:
                self.screen.blit(self.BULLET, (bullet.x_position, bullet.y_position))
                if bullet.x_position > self.W_W:
                    red_spaceship.bullets.remove(bullet) 

            """Drawing Rocks in the Screen"""
            for rock in rocks_1:
                self.screen.blit(self.ROCK_1, (rock.x_position, rock.y_position))
            for rock in rocks_2:
                self.screen.blit(self.ROCK_2, (rock.x_position, rock.y_position))
            for rock in rocks_3:
                self.screen.blit(self.ROCK_3, (rock.x_position, rock.y_position))

            """Drawing Score"""
            text = font.render("Score: " + str(self.Score), True, "white")
            textRect = text.get_rect()
            textRect.center = (self.W_W//2, 40)
            self.screen.blit(text, textRect)

            """Drawing Health"""         
            health = pygame.Rect(self.W_W//2 - 100, 10, 200 , 10)
            pygame.draw.rect(self.screen, "red",health)

            health = pygame.Rect(self.W_W//2 - 100, 10, 20*self.Health , 10)
            pygame.draw.rect(self.screen, "white",health)

            """Drawing Pause"""
            pause = Pause.render("Pause", True, "white")
            pauseRect = pause.get_rect()
            pauseRect.center = (self.W_W//2, self.W_H//2)
            self.screen.blit(pause, pauseRect)
            pygame.display.update()


    def main_menu(self,):
        active = True
        new_game = pygame.font.SysFont("dejavuserif", 50)
        leader_board = pygame.font.SysFont("dejavuserif", 50)
        new_game_color = "white"
        leader_board_color = "white"
        
        while active:
            self.clock.tick(self.FPS) # Setting the Frame Rate

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Active = False
                    pygame.quit()

                # Selecting to play the game or to view leaderboard
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if self.W_H//2 - 150< mouse[1] <self.W_H//2 - 50 and self.W_W//2 - 150 < mouse[0] < self.W_W//2 + 150:
                        active = False
                        self.Health = 10
                        self.Score = 0
                        self.running_game()
                    elif self.W_H//2 - 30< mouse[1] <self.W_H//2 + 30 and self.W_W//2 - 200 < mouse[0] < self.W_W//2 + 200:
                        active = False
                        self.board()

            mouse = pygame.mouse.get_pos()
            
            # If mouse is on the New Game or LeaderBoard make text blue
            if  self.W_H//2 - 150< mouse[1] <self.W_H//2 - 80 and self.W_W//2 - 150 < mouse[0] < self.W_W//2 + 150:
                new_game_color = "blue"
            elif self.W_H//2 - 30< mouse[1] <self.W_H//2 + 30 and self.W_W//2 - 200 < mouse[0] < self.W_W//2 + 200:
                leader_board_color = "blue"
            else:
                new_game_color = "white"
                leader_board_color = "white"

            # Creating the New Game Button
            New_Game = new_game.render("New Game", True, new_game_color)
            new_game_rect = New_Game.get_rect()
            new_game_rect.center = (self.W_W//2, self.W_H//2 - 100)

            # Creating Leader Board Button
            Leader_Board = leader_board.render("Leader Board", True, leader_board_color)
            leader_board_rect = Leader_Board.get_rect()
            leader_board_rect.center = (self.W_W//2, self.W_H//2)
            
            # Displaying Everthing on the Screen
            self.screen.blit(self.BACKGROUND_1, (0,0))
            self.screen.blit(New_Game, new_game_rect)
            self.screen.blit(Leader_Board, leader_board_rect)
            
            pygame.display.update()
    

    def board(self):
        active = True
        leader_font = list()
        back_color = "white"
        back_button = pygame.font.SysFont("dejavuserif", 80)
        
        while active:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Active = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.W_H - 100 < mouse[1] < self.W_H - 20 and self.W_W - 250 < mouse[0] < self.W_W - 50:
                        active = False
                        self.main_menu()

            self.screen.blit(self.BACKGROUND_1,(0,0))
            
            mouse = pygame.mouse.get_pos()
            
            if self.W_H - 100 < mouse[1] < self.W_H - 20 and self.W_W - 250 < mouse[0] < self.W_W - 50:
                back_color = "blue"
            else:
                back_color = "white"


            info = back_button.render("Back", True, back_color)
            back_rect = info.get_rect()
            back_rect.center = (self.W_W - 150, self.W_H - 60)
            self.screen.blit(info, back_rect)    
            

            for i in range(len(self.leader_board)):
                leader_font.append(pygame.font.SysFont("dejavuserif", 35))
                information = leader_font[i].render(str(i+1) + ") " + self.leader_board[i][0] + ":" + " "*20 + str(self.leader_board[i][1]) + " "*20 + self.leader_board[i][2], True, "blue")
                rect = information.get_rect()
                rect.center = (self.W_W//2 , self.W_H//15 + i*100)
                self.screen.blit(information, rect)
            pygame.display.update()


    def add_score(self,):
        active = True
        base_font = pygame.font.Font(None, 40)
        text_font = pygame.font.Font(None, 40)
        user_input = ''
        input_rect = pygame.Rect(self.W_W//2 - 100, self.W_H//2, 150, 40)
        done_button = pygame.font.SysFont("dejavuserif", 80)
        while active:
            self.clock.tick(self.FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Active = False
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_input =  user_input[0:-1]
                    else:
                        if len(user_input) <= 8:
                            user_input += event.unicode               

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.W_H - 100 < mouse[1] < self.W_H - 20 and self.W_W - 250 < mouse[0] < self.W_W - 50:
                        self.storing_scores(user_input)
                        self.main_menu()
            
            self.screen.blit(self.BACKGROUND_1,(0,0))

            """Drawing the text user is writing"""
            text_surface = base_font.render(user_input, True, "red")                
            text_text_surface = text_font.render("Type Your Name", True, "white")
            self.screen.blit(text_text_surface,(self.W_W//2 - 140, self.W_H//2 - 50))
            
            """Drawing the Rectacngle for the text"""
            pygame.draw.rect(self.screen, "white", input_rect, 3)
            self.screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

            """Controlling if the user has his mouse on Button Done"""
            mouse = pygame.mouse.get_pos()
            if self.W_H - 100 < mouse[1] < self.W_H - 20 and self.W_W - 250 < mouse[0] < self.W_W - 50:
                done_color = "blue"
            else:
                done_color = "white"

            info = done_button.render("Done", True, done_color)
            done_rect  = info.get_rect()
            done_rect.center = (self.W_W - 150, self.W_H - 60)
            self.screen.blit(info, done_rect)    
                        
            pygame.display.update()


    def storing_scores(self,user_input):
        today = date.today()
        # dd/mm/YY
        d1 = today.strftime("%d/%m/%Y")
        data = self.leader_board

        data.append([user_input,self.Score, d1])
        data = self.select_short(data)
        if len(data) > 8:
            data = data[0:-1]

        with open(os.path.join("game_files", "leader_board.json"), "w") as file:
            json.dump(data, file)

    def select_short(self,array):
        for i in range(len(array)):
      
            min_idx = i
            for j in range(i+1, len(array)):
                if array[min_idx][1] < array[j][1]:
                    min_idx = j
                    
            # Swap the found minimum element with 
            # the first element        
            array[i], array[min_idx] = array[min_idx], array[i]

        return array