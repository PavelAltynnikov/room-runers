from typing import Callable, Optional

from src.model.interface import IBoundary, BoundaryPosition, ILevel, IRoom, ICharacter, ITimer
from src.model.level import Wall, Door, Portal, PortalsKeeper


class Controller:
    def __init__(self, character: ICharacter):
        self._character = character
        self._required_answers = "wasdvq"
        self.quit_action: Optional[Callable[..., None]] = None

    def query_input_device(self):

        answer = input(
            f"\nХодит персонаж {self._character.name}\n"
            "Что делать персонажу?\n"
            "w. Идти вверх\n"
            "d. Идти вправо\n"
            "s. Идти вниз\n"
            "a. Идти влево\n"
            "v. Ждать\n"
            "q. Сдаться\n"
            "Ответ буквой: "
        )
        print()

        if answer not in self._required_answers:
            print(f"Ваш ответ не понятен, введите один из символов {self._required_answers}\n")
            return

        if answer == "q":
            if self.quit_action:
                self.quit_action()
            return

        if answer == "w":
            self._character.try_to_go_up()
        elif answer == "d":
            self._character.try_to_go_right()
        elif answer == "s":
            self._character.try_to_go_down()
        elif answer == "a":
            self._character.try_to_go_left()
        elif answer == "v":
            print("Ну ждите...\n")


class EndGameException(Exception):
    pass


class LevelView:
    def __init__(
        self,
        level: ILevel,
        portals_keeper: PortalsKeeper,
        game_timer: ITimer,
        controller_1: Controller,
        controller_2: Controller
    ):
        self._level = level
        self._portals_keeper = portals_keeper
        self._controller_1 = controller_1
        self._controller_1.quit_action = self.quit
        self._controller_2 = controller_2
        self._controller_2.quit_action = self.quit
        self._game_timer = game_timer

        self.characters_encounter_delegate: Callable[..., bool] | None = None
        self.game_times_up: Callable[..., bool] | None = None

    def show(self):
        try:
            while True:
                self._player_turn(self._controller_1)
                self._player_turn(self._controller_2)

                self._portals_keeper.try_to_open_portals()
                self._game_timer.update()

                if self.game_times_up:
                    if self.game_times_up():
                        self.quit()

                print(
                    f"Осталось ходов: {self._game_timer.end_time - self._game_timer.current_time}"
                )

        except EndGameException:
            print("Игра закончена")
        finally:
            input()

    def quit(self):
        raise EndGameException()

    def _player_turn(self, controller: Controller):
        self._draw_level()
        controller.query_input_device()

        if self.characters_encounter_delegate is None:
            return

        result = self.characters_encounter_delegate()
        if result:
            raise EndGameException()

    def _draw_level(self):
        for row in self._level.rooms:
            print("┌" + "┐ ┌".join([self._draw_boundary(room.boundary_up) for room in row]) + "┐")
            print(
                " ".join([
                    f"{self._draw_boundary(room.boundary_left)} "
                    f"{self._draw_character(room)} "
                    f"{self._draw_boundary(room.boundary_right)}"
                    for room in row
                ])
            )
            print("└" + "┘ └".join([self._draw_boundary(room.boundary_down) for room in row]) + "┘")

    def _draw_boundary(self, boundary: IBoundary | None) -> str:
        if boundary is None:
            raise Exception("Невозможно отрисовать несуществующую перегородку.")

        if boundary.position is BoundaryPosition.HORIZONTAL:
            if isinstance(boundary, Wall):
                return str("═══")
            if isinstance(boundary, Portal):
                return str(" - ")
            if isinstance(boundary, Door):
                return str("   ")

        if isinstance(boundary, Wall):
            return str("║")
        if isinstance(boundary, Portal):
            return str("⁞")
        if isinstance(boundary, Door):
            return str(" ")

        raise Exception(f"Невозможно отрисовать перегородку с типом: {boundary}")

    def _draw_character(self, room: IRoom):
        character = self._level.get_character_from_room(room)

        if character is None:
            return " "

        return character.name[0]
