from model.game_objects import Character
from model.level import Level
from view import LevelView, Controller

VERSION = "0.1.1"


def main():
    size = 10
    character = Character()
    controller = Controller(character)
    level = Level(size, character)

    w = LevelView(level, controller)
    w.show()


if __name__ == "__main__":
    main()
