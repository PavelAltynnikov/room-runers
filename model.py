"""Переход из одной комнаты в другую осуществляется через перегородки.
Перегородки нужны чтобы хранить ссылки на комнаты.
Почему нельзя это делать без перегородок, потому что у разных перегородок в UI есть
разный доступ. Какие-то совсем не доступны для перехода, через какие-то можно проходить
с определённым условием.

Как происходит переход.
1. Пользовать нажимает кнопку направления.
2. Игрок знает в какой комнате находится, выбирает ограждающую конструкцию в зависимости
от направления движения.
3. Пытается перейти через неё.
    3.1 Если ограждение - это стена, то ничего не произойдёт;
    3.2 Если ограждение - это дверь, то игрок перейдёт в другую комнату.
"""
import random
from abc import ABC, abstractmethod
from enum import Enum
from typing import Protocol, Optional, Type


class Position(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class ICharacter(Protocol):
    def change_room(self, room: Type["IRoom"]):
        ...

    def try_to_go_up(self):
        ...

    def try_to_go_right(self):
        ...

    def try_to_go_down(self):
        ...

    def try_to_go_left(self):
        ...


class IRoom(Protocol):
    """Представляет ячейку игрового поля в которой может находится персонаж.
    Задача комнаты хранить персонажа и ограждения."""
    def try_to_release_character_up(self, character: ICharacter) -> None:
        """Выпустить игрока из комнаты в комнату сверху"""
        ...

    def try_to_release_character_right(self, character: ICharacter) -> None:
        """Выпустить игрока из комнаты в комнату справа"""
        ...

    def try_to_release_character_down(self, character: ICharacter) -> None:
        """Выпустить игрока из комнаты в комнату снизу"""
        ...

    def try_to_release_character_left(self, character: ICharacter) -> None:
        """Выпустить игрока из комнаты в комнату слева"""
        ...


class Boundary(ABC):
    """Представляет перегородку между двумя комнатами.
    Задача ограждения передать игрока из одной комнаты в другую.
    """
    def __init__(self):
        self._position: Optional[Position] = None
        self._room_1: Optional[IRoom] = None
        self._room_2: Optional[IRoom] = None

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position: Position):
        self._position = position

    @property
    def room_1(self):
        return self._room_1

    @room_1.setter
    def room_1(self, room: IRoom):
        self._room_1 = room

    @property
    def room_2(self):
        return self._room_2

    @room_2.setter
    def room_2(self, room: IRoom):
        self._room_2 = room

    @abstractmethod
    def move_character_to_another_room(
            self, character: ICharacter, current_room: IRoom) -> None:
        """Перемещение модели игрока в соседнюю комнату.

        Args:
            character (ICharacter): Модель игрока.
            current_room (IRoom): Комната в которой сейчас находится модель игрока.
        """
        ...

    def __str__(self):
        return f"{type(self)}, {self._position}"


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Room(IRoom):
    def __init__(self, point: Point):
        self.location = point
        self._boundary_up = None
        self._boundary_right = None
        self._boundary_down = None
        self._boundary_left = None

    @property
    def boundary_up(self):
        return self._boundary_up

    @boundary_up.setter
    def boundary_up(self, value: Boundary):
        self._boundary_up = value

    @property
    def boundary_right(self):
        return self._boundary_right

    @boundary_right.setter
    def boundary_right(self, value: Boundary):
        self._boundary_right = value

    @property
    def boundary_down(self):
        return self._boundary_down

    @boundary_down.setter
    def boundary_down(self, value: Boundary):
        self._boundary_down = value

    @property
    def boundary_left(self):
        return self._boundary_left

    @boundary_left.setter
    def boundary_left(self, value: Boundary):
        self._boundary_left = value

    def try_to_release_character_up(self, character: ICharacter) -> None:
        if self._boundary_up:
            self._boundary_up.move_character_to_another_room(character, self)

    def try_to_release_character_right(self, character: ICharacter) -> None:
        if self._boundary_right:
            self._boundary_right.move_character_to_another_room(character, self)

    def try_to_release_character_down(self, character: ICharacter) -> None:
        if self._boundary_down:
            self._boundary_down.move_character_to_another_room(character, self)

    def try_to_release_character_left(self, character: ICharacter) -> None:
        if self._boundary_left:
            self._boundary_left.move_character_to_another_room(character, self)

    def __str__(self):
        return "{}, {}, {}, {}, {}".format(
            self.location,
            self._boundary_up,
            self._boundary_right,
            self._boundary_down,
            self._boundary_left
        )


class Character(ICharacter):
    def __init__(self, room: IRoom):
        self._room = room

    def change_room(self, room: IRoom):
        self._room = room

    def try_to_go_up(self):
        self._room.try_to_release_character_up(self)

    def try_to_go_right(self):
        self._room.try_to_release_character_right(self)

    def try_to_go_down(self):
        self._room.try_to_release_character_down(self)

    def try_to_go_left(self):
        self._room.try_to_release_character_left(self)


class Wall(Boundary):
    def move_character_to_another_room(
            self, character: ICharacter, current_room: IRoom) -> None:
        """Перегородка не пропускает через себя, поэтому метод не меняет комнату."""
        return None

    def __str__(self):
        if self._position is Position.UP or self._position is Position.DOWN:
            return "═══"
        return "║"


class Door(Boundary):
    def move_character_to_another_room(
            self, character: ICharacter, current_room: IRoom) -> None:
        if (current_room is self._room_1
                and self._room_2 is not None):
            character.change_room(self._room_2)
        elif (current_room is self._room_2
                and self._room_1 is not None):
            character.change_room(self._room_1)

    def __str__(self):
        if self._position is Position.UP or self._position is Position.DOWN:
            return "   "
        return " "


class Portal(Door):
    def move_character_to_another_room(
            self, character: ICharacter, current_room: IRoom) -> None:
        # тут нужен какой-то таймер
        super().move_character_to_another_room(character, current_room)

    def __str__(self):
        if self._position is Position.UP or self._position is Position.DOWN:
            return " - "
        return "⁞"


class BoundaryGenerator:
    def __init__(self, size: int):
        self._size = size - 1
        self._boundaries: list[Boundary] = [Wall, Door, Portal]  # type: ignore

    def get_boundary(self, location: Point, position: Position) -> Boundary:
        if (location.x == 0 and position is Position.LEFT
           or location.y == 0 and position is Position.UP
           or location.x == self._size and position is Position.RIGHT
           or location.y == self._size and position is Position.DOWN):
            boundary = Wall()
            boundary.position = position
            return boundary

        boundary_type = random.choice(self._boundaries)
        boundary = boundary_type()  # type: ignore
        boundary.position = position
        return boundary  # type: ignore


class Level:
    def __init__(self, size: int):
        self._rooms = self._generate(size)

    def _generate(self, size: int) -> list[list[IRoom]]:
        rooms: list[list[IRoom]] = []
        bg = BoundaryGenerator(size)

        for y in range(size):
            row: list[Room] = []

            for x in range(size):

                point = Point(x, y)

                room = Room(
                    coordinates=point,
                    boundary_left=bg.get_boundary(point, Position.LEFT),
                    boundary_up=bg.get_boundary(point, Position.UP),
                    boundary_down=bg.get_boundary(point, Position.DOWN),
                    boundary_right=bg.get_boundary(point, Position.RIGHT),
                )

                row.append(room)

            rooms.append(row)  # type: ignore

        return rooms

    def print(self):
        for row in self._rooms:
            for room in row:
                print(room)
            print()


if __name__ == "__main__":
    size = 10
    level = Level(size)
    level.print()
