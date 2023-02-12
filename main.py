from src.model.game_objects import Character, GameRules
from src.model.level import Level
from src.view import LevelView, Controller

VERSION = "0.1.1"


def main():
    character_1 = Character("Ripley")
    character_2 = Character("Alien")

    game_rules = GameRules(character_1, character_2)

    size = 10
    level = Level(size, character_1, character_2)

    controller_1 = Controller(character_1)
    controller_2 = Controller(character_2)

    w = LevelView(level, controller_1, controller_2)
    w.characters_encounter_delegate = game_rules.check_characters_encounter
    w.show()


if __name__ == "__main__":
    main()
