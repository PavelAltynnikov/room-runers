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
from abc import ABC, abstractmethod
from typing import Optional
import random

from .interface import IBoundary, BoundaryPosition, ICharacter, IRoom, ILevel, ITimer
from .game_objects import Timer


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{type(self)}, x={self.x}, y={self.y}"


class Room(IRoom):
    def __init__(self, point: Point):
        self._location = point
        self._boundary_up = None
        self._boundary_right = None
        self._boundary_down = None
        self._boundary_left = None

    @property
    def boundary_up(self):
        return self._boundary_up

    @boundary_up.setter
    def boundary_up(self, value: IBoundary):
        self._boundary_up = value

    @property
    def boundary_right(self):
        return self._boundary_right

    @boundary_right.setter
    def boundary_right(self, value: IBoundary):
        self._boundary_right = value

    @property
    def boundary_down(self):
        return self._boundary_down

    @boundary_down.setter
    def boundary_down(self, value: IBoundary):
        self._boundary_down = value

    @property
    def boundary_left(self):
        return self._boundary_left

    @boundary_left.setter
    def boundary_left(self, value: IBoundary):
        self._boundary_left = value

    def get_location(self) -> tuple[int, int]:
        return self._location.x, self._location.y

    def get_x_coordinate(self) -> int:
        return self._location.x

    def get_y_coordinate(self) -> int:
        return self._location.y

    def try_to_release_character_up(self, character: ICharacter) -> None:
        if self._boundary_up:
            self._boundary_up.character_wants_to_pass(character)
            self._boundary_up.move_character_to_another_room()

    def try_to_release_character_right(self, character: ICharacter) -> None:
        if self._boundary_right:
            self._boundary_right.character_wants_to_pass(character)
            self._boundary_right.move_character_to_another_room()

    def try_to_release_character_down(self, character: ICharacter) -> None:
        if self._boundary_down:
            self._boundary_down.character_wants_to_pass(character)
            self._boundary_down.move_character_to_another_room()

    def try_to_release_character_left(self, character: ICharacter) -> None:
        if self._boundary_left:
            self._boundary_left.character_wants_to_pass(character)
            self._boundary_left.move_character_to_another_room()

    def __str__(self):
        return "{}, {}, {}, {}, {}".format(
            self._location,
            self._boundary_up,
            self._boundary_right,
            self._boundary_down,
            self._boundary_left
        )


class Boundary(ABC, IBoundary):
    def __init__(self):
        self._position: BoundaryPosition | None = None
        self._room_1: IRoom | None = None
        self._room_2: IRoom | None = None
        self._character: ICharacter | None = None

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

    def __str__(self):
        return f"{type(self)}, {self._position}"

    def character_wants_to_pass(self, character: ICharacter):
        self._character = character

    def character_is_gone(self):
        self._character = None

    @abstractmethod
    def move_character_to_another_room(self) -> None:
        ...


class Wall(Boundary):
    def __init__(self):
        super().__init__()

    def move_character_to_another_room(self) -> None:
        """Стена не пропускает через себя, поэтому метод не меняет комнату."""
        self.character_is_gone()
        return None


class Door(Boundary):
    def __ini__(self):
        super().__init__()

    def move_character_to_another_room(self) -> None:
        if self._character is None:
            return

        if (
            self._character.current_room is self._room_1
            and self._room_2 is not None
        ):
            self._character.change_room(self._room_2)
        elif (
            self._character.current_room is self._room_2
            and self._room_1 is not None
        ):
            self._character.change_room(self._room_1)

        self.character_is_gone()


class Portal(Door):
    def __init__(self, timer: ITimer):
        super().__init__()
        self._timer = timer

    @property
    def timer(self) -> ITimer:
        return self._timer

    def character_is_gone(self):
        super().character_is_gone()
        self._timer.reset()

    def move_character_to_another_room(self) -> None:
        if self._character is None:
            # TODO надо подумать, стоит ли тут выкидывать исключение.
            # TODO не нравится мне этот reset.
            # Нужно чтобы кто-то запускал метод character_is_gone данного класса.
            # Потому что сейчас данный метод запускается только после пересечения перегородки.
            self._timer.reset()
            return

        if not self._timer.is_active:
            self._timer.start()

        if self._timer.is_times_up():
            super().move_character_to_another_room()
            self._timer.reset()


class BoundaryGenerator:
    def __init__(self, size: int):
        self._max_walls_percent = 20  # процент должен быть для каждого ряда и столбца отдельно
        self._internal_boundaries_amount = self._calculate_internal_boundaries_amount(size)
        self._internal_walls_amount = 0
        self._boundaries: list[Boundary] = [Wall, Door, Portal]  # type: ignore

    @staticmethod
    def _calculate_internal_boundaries_amount(size: int) -> int:
        return size * (size - 1) + size * (size - 1)

    def _calculate_walls_percent(self):
        return self._internal_walls_amount * 100 / self._internal_boundaries_amount

    def get_boundary(self, position: BoundaryPosition) -> IBoundary:
        boundary_type = random.choice(self._boundaries)

        if boundary_type is Wall:
            percent = self._calculate_walls_percent()
            if percent > self._max_walls_percent:
                return self.get_boundary(position)
            else:
                self._internal_walls_amount += 1

        if boundary_type is Portal:
            boundary = boundary_type(Timer(amount_of_time=2))  # type: ignore
        else:
            boundary = boundary_type()  # type: ignore

        boundary.position = position

        return boundary  # type: ignore


class Level(ILevel):
    def __init__(self, size: int, character_1: ICharacter, character_2: ICharacter):
        self._size = size
        self._character_1 = character_1
        self._character_2 = character_2
        self._rooms = self._generate()
        self._set_characters_into_room()

    @property
    def rooms(self) -> list[list[IRoom]]:
        return self._rooms

    def get_character_from_room(self, room: IRoom) -> Optional[ICharacter]:
        # у character нужно сделать свойство current_room
        if self._character_1._room is room:  # type: ignore
            return self._character_1
        if self._character_2._room is room:  # type: ignore
            return self._character_2

    def _generate(self) -> list[list[IRoom]]:
        rooms = self._arrange_rooms()
        self._arrange_external_boundaries(rooms)
        self._arrange_internal_boundaries(rooms)
        return rooms

    def _arrange_rooms(self) -> list[list[IRoom]]:
        rooms: list[list[IRoom]] = []

        for y in range(self._size):
            row: list[IRoom] = []
            for x in range(self._size):
                row.append(Room(Point(x, y)))
            rooms.append(row)

        return rooms

    def _arrange_external_boundaries(self, rooms: list[list[IRoom]]) -> None:
        for row in rooms:
            for room in row:
                if room.get_y_coordinate() == 0:
                    boundary = Wall()
                    boundary.position = BoundaryPosition.HORIZONTAL
                    room.boundary_up = boundary
                    boundary.room_1 = room

                if room.get_x_coordinate() == 0:
                    boundary = Wall()
                    boundary.position = BoundaryPosition.VERTICAL
                    room.boundary_left = boundary
                    boundary.room_1 = room

                if room.get_y_coordinate() == self._size - 1:
                    boundary = Wall()
                    boundary.position = BoundaryPosition.HORIZONTAL
                    room.boundary_down = boundary
                    boundary.room_1 = room

                if room.get_x_coordinate() == self._size - 1:
                    boundary = Wall()
                    boundary.position = BoundaryPosition.VERTICAL
                    room.boundary_right = boundary
                    boundary.room_1 = room

    def _arrange_internal_boundaries(self, rooms: list[list[IRoom]]) -> None:
        bg = BoundaryGenerator(self._size)
        self._arrange_vertical_boundaries(rooms, bg)
        self._arrange_horizontal_boundaries(rooms, bg)

    def _arrange_vertical_boundaries(
        self,
        rooms: list[list[IRoom]],
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
        rooms: list[list[IRoom]],
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

    def _set_characters_into_room(self):
        self._character_1.change_room(self._find_random_room())
        self._character_2.change_room(self._find_random_room())

    def _find_random_room(self) -> IRoom:
        return self._rooms[random.randint(0, self._size - 1)][random.randint(0, self._size - 1)]
