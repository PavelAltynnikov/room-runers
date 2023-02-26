from src.model.game_objects import Character, GameRules, Timer
from src.model.level import Level, PortalsKeeper
from src.view import LevelView, Controller

VERSION = "0.2.0"


def main():
    character_1 = Character("Ripley")
    character_2 = Character("Alien")

    game_timer = Timer(10)
    game_rules = GameRules(game_timer, character_1, character_2)

    portals_keeper = PortalsKeeper()

    size = 10
    level = Level(size, character_1, character_2, portals_keeper)

    controller_1 = Controller(character_1)
    controller_2 = Controller(character_2)

    w = LevelView(level, portals_keeper, game_timer, controller_1, controller_2)
    w.characters_encounter_delegate = game_rules.check_characters_encounter
    w.game_times_up = game_rules.check_times_up
    w.show()


if __name__ == "__main__":
    main()
