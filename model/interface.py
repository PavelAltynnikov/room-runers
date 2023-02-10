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


class IRoom(Protocol):
    """Представляет ячейку игрового поля в которой может находится персонаж.
    Задача комнаты хранить персонажа и ограждения."""
    boundary_up: Boundary
    boundary_right: Boundary
    boundary_down: Boundary
    boundary_left: Boundary

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
