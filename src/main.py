from game import Game

"""Global Variablea"""
W_W = 1500 # Window Width
W_H = 800 # Window height
FPS = 40 # The Frames per Second of the game



def main():
    game = Game(W_H, W_W, FPS)
    game.main_menu()


if __name__ == "__main__":
    main()
       