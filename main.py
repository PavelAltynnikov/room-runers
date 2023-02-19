from src.model.game_objects import Character, GameRules, Timer
from src.model.level import Level
from src.view import LevelView, Controller

VERSION = "0.1.1"


def main():
    character_1 = Character("Ripley")
    character_2 = Character("Alien")

    game_timer = Timer(5)
    game_rules = GameRules(game_timer, character_1, character_2)

    size = 10
    level = Level(size, character_1, character_2)

    controller_1 = Controller(character_1)
    controller_2 = Controller(character_2)

    w = LevelView(level, game_timer, controller_1, controller_2)
    w.characters_encounter_delegate = game_rules.check_characters_encounter
    w.game_times_up = game_rules.check_times_up
    w.show()


if __name__ == "__main__":
    main()
