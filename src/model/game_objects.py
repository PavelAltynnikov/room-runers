from .interface import ICharacter, IRoom, ITimer


class Character(ICharacter):
    def __init__(self, name: str):
        self.name = name
        self._room = None

    def change_room(self, room: IRoom):
        self._room = room

    def try_to_go_up(self):
        if self._room:
            self._room.try_to_release_character_up(self)

    def try_to_go_right(self):
        if self._room:
            self._room.try_to_release_character_right(self)

    def try_to_go_down(self):
        if self._room:
            self._room.try_to_release_character_down(self)

    def try_to_go_left(self):
        if self._room:
            self._room.try_to_release_character_left(self)


class Timer(ITimer):
    def __init__(self, amount_of_time: int):
        self._end_time = amount_of_time
        self._current_time = 0
        self._is_active = False

    @property
    def is_active(self):
        return self._is_active

    @property
    def current_time(self):
        return self._current_time

    def start(self):
        self._is_active = True

    def is_times_up(self):
        return self._current_time >= self._end_time

    def update(self):
        if self._is_active:
            self._current_time += 1

    def reset(self):
        self._current_time = 0
        self._is_active = False


class GameRules:
    def __init__(self, timer: ITimer, character_1: ICharacter, character_2: ICharacter):
        self._timer = timer
        self._character_1 = character_1
        self._character_2 = character_2

    def check_characters_encounter(self):
        return self._character_1._room is self._character_2._room  # type: ignore

    def check_times_up(self):
        if not self._timer.is_active:
            self._timer.start()

        if self._timer.is_times_up():
            return True

        return False
