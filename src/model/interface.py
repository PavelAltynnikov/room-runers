from enum import Enum
from typing import Protocol, ForwardRef, Optional


IRoom = ForwardRef("IRoom")  # type: ignore


class BoundaryPosition(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class ICharacter(Protocol):
    name: str

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


class IBoundary(Protocol):
    @property
    def position(self) -> Optional[BoundaryPosition]:
        ...

    @property
    def room_1(self) -> Optional[IRoom]:
        ...

    @room_1.setter
    def room_1(self, room: IRoom) -> None:
        ...

    @property
    def room_2(self) -> Optional[IRoom]:
        ...

    @room_2.setter
    def room_2(self, room: IRoom) -> None:
        ...

    def move_character_to_another_room(self, character: ICharacter, current_room: IRoom) -> None:
        """Перемещение модели игрока в соседнюю комнату.

        Args:
            character (ICharacter): Модель игрока.
            current_room (IRoom): Комната в которой сейчас находится модель игрока.
        """
        ...


class IRoom(Protocol):
    """Представляет ячейку игрового поля в которой может находится персонаж.
    Задача комнаты хранить персонажа и ограждения."""
    @property
    def boundary_up(self) -> IBoundary | None:
        ...

    @boundary_up.setter
    def boundary_up(self, value: IBoundary) -> None:
        ...

    @property
    def boundary_right(self) -> IBoundary | None:
        ...

    @boundary_right.setter
    def boundary_right(self, value: IBoundary) -> None:
        ...

    @property
    def boundary_down(self) -> IBoundary | None:
        ...

    @boundary_down.setter
    def boundary_down(self, value: IBoundary) -> None:
        ...

    @property
    def boundary_left(self) -> IBoundary | None:
        ...

    @boundary_left.setter
    def boundary_left(self, value: IBoundary) -> None:
        ...

    def get_location(self) -> tuple[int, int]:
        ...

    def get_x_coordinate(self) -> int:
        ...

    def get_y_coordinate(self) -> int:
        ...

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


class ILevel(Protocol):
    @property
    def rooms(self) -> list[list[IRoom]]:
        ...

    def get_character_from_room(self, room: IRoom) -> Optional[ICharacter]:
        ...


class ITimer:
    @property
    def is_active(self) -> bool:
        ...

    @property
    def current_time(self) -> int:
        ...

    @property
    def end_time(self) -> int:
        ...

    def start(self) -> None:
        ...

    def is_times_up(self) -> bool:
        ...

    def update(self) -> None:
        ...

    def reset(self) -> None:
        ...
