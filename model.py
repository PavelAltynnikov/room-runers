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
from typing import Protocol, Optional, ForwardRef


IRoom = ForwardRef("IRoom")  # type: ignore


class BoundaryPosition(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class ICharacter(Protocol):
    def change_room(self, room: IRoom):
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
        self._position: Optional[BoundaryPosition] = None
        self._room_1: Optional[IRoom] = None
        self._room_2: Optional[IRoom] = None

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position: BoundaryPosition):
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

    def __str__(self):
        return f"{type(self)}, x={self.x}, y={self.y}"


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
        if self._position is BoundaryPosition.HORIZONTAL:
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
        if self._position is BoundaryPosition.HORIZONTAL:
            return str("   ")
        return str(" ")


class Portal(Door):
    def move_character_to_another_room(
            self, character: ICharacter, current_room: IRoom) -> None:
        # тут нужен какой-то таймер
        super().move_character_to_another_room(character, current_room)

    def __str__(self):
        if self._position is BoundaryPosition.HORIZONTAL:
            return str(" - ")
        return str("⁞")


class BoundaryGenerator:
    def __init__(self, size: int):
        self._size = size - 1
        self._boundaries: list[Boundary] = [Wall, Door, Portal]  # type: ignore

    def get_boundary(self, position: BoundaryPosition) -> Boundary:
        boundary_type = random.choice(self._boundaries)
        boundary = boundary_type()  # type: ignore
        boundary.position = position
        return boundary  # type: ignore


class Level:
    def __init__(self, size: int):
        self._size = size
        self._rooms = self._generate()

    def _generate(self) -> list[list[Room]]:
        rooms = self._arrange_rooms()
        self._arrange_external_boundaries(rooms)
        self._arrange_internal_boundaries(rooms)
        return rooms

    def _arrange_rooms(self) -> list[list[Room]]:
        rooms: list[list[Room]] = []

        for y in range(self._size):
            row: list[Room] = []
            for x in range(self._size):
                row.append(Room(Point(x, y)))
            rooms.append(row)

        return rooms

    def _arrange_external_boundaries(self, rooms: list[list[Room]]) -> None:
        for row in rooms:
            for room in row:
                if room.location.y == 0:
                    boundary = Wall()
                    boundary.position = BoundaryPosition.HORIZONTAL
                    room.boundary_up = boundary
                    boundary.room_1 = room

                if room.location.x == 0:
                    boundary = Wall()
                    boundary.position = BoundaryPosition.VERTICAL
                    room.boundary_left = boundary
                    boundary.room_1 = room

                if room.location.y == self._size - 1:
                    boundary = Wall()
                    boundary.position = BoundaryPosition.HORIZONTAL
                    room.boundary_down = boundary
                    boundary.room_1 = room

                if room.location.x == self._size - 1:
                    boundary = Wall()
                    boundary.position = BoundaryPosition.VERTICAL
                    room.boundary_right = boundary
                    boundary.room_1 = room

    def _arrange_internal_boundaries(self, rooms: list[list[Room]]) -> None:
        bg = BoundaryGenerator(self._size)
        self._arrange_vertical_boundaries(rooms, bg)
        self._arrange_horizontal_boundaries(rooms, bg)

    def _arrange_vertical_boundaries(
        self,
        rooms: list[list[Room]],
        b_generator: BoundaryGenerator
    ) -> None:
        for row in rooms:

            adjacent_rooms = [
                (row[i], row[i + 1])
                for i
                in range(len(row) - 1)
            ]

            for rooms_pair in adjacent_rooms:
                boundary = b_generator.get_boundary(BoundaryPosition.VERTICAL)

                boundary.room_1 = rooms_pair[0]
                rooms_pair[0].boundary_right = boundary

                boundary.room_2 = rooms_pair[1]
                rooms_pair[1].boundary_left = boundary

    def _arrange_horizontal_boundaries(
        self,
        rooms: list[list[Room]],
        b_generator: BoundaryGenerator
    ) -> None:

        adjacent_rows = [
            (rooms[i], rooms[i + 1])
            for i
            in range(len(rooms) - 1)
        ]

        for rows_pair in adjacent_rows:
            for rooms_pair in zip(*rows_pair):
                boundary = b_generator.get_boundary(BoundaryPosition.HORIZONTAL)

                boundary.room_1 = rooms_pair[0]
                rooms_pair[0].boundary_down = boundary

                boundary.room_2 = rooms_pair[1]
                rooms_pair[1].boundary_up = boundary

    def print(self):
        for row in self._rooms:
            print("┌" + "┐ ┌".join([str(room.boundary_up) for room in row]) + "┐")
            print(
                " ".join([
                    f"{room.boundary_left}   {room.boundary_right}"
                    for room in row
                ])
            )
            print("└" + "┘ └".join([str(room.boundary_down) for room in row]) + "┘")


if __name__ == "__main__":
    size = 10
    level = Level(size)
    level.print()
