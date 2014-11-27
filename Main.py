__author__ = 'Андрей'

from Scene import LoadScene,MainMenu
from Game import Game

def main():

    scene = LoadScene(3000,MainMenu())
    game = Game(scene=scene)
    game.set_caption(title="Revers")
    game.game_loop()

if __name__ == "__main__":
    main()