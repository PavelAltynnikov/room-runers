from typing import Callable, Optional

from src.model.interface import Boundary, BoundaryPosition, ILevel, IRoom, ICharacter
from src.model.level import Wall, Door, Portal


class Controller:
    def __init__(self, character: ICharacter):
        self._character = character
        self._required_answers = "wasdq"
        self.quit_action: Optional[Callable] = None

    def query_input_device(self):

        answer = input(
            "Куда передвинуть персонажа?\n"
            "w. Вверх\n"
            "d. Вправо\n"
            "s. Вниз\n"
            "a. Влево\n"
            "q. Закрыть игру\n"
            "Ответ буквой: "
        )

        if answer not in self._required_answers:
            print(f"Ваш ответ не понятен, введите один из символов {self._required_answers}")
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


class LevelView:
    def __init__(self, level: ILevel, controller: Controller):
        self._level = level
        self._controller = controller
        self._controller.quit_action = self.quit
        self._is_showing = True

    def show(self):
        while self._is_showing:
            self._draw_level()
            self._controller.query_input_device()

    def quit(self):
        self._is_showing = False

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

    def _draw_boundary(self, boundary: Boundary) -> str:
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
        if self._level.is_character_in_this_room(room):
            return "c"
        return " "
