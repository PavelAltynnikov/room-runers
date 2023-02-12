from .interface import ICharacter, IRoom


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


class GameRules:
    def __init__(self, character_1: ICharacter, character_2: ICharacter):
        self._character_1 = character_1
        self._character_2 = character_2

    def check_characters_encounter(self):
        return self._character_1._room is self._character_2._room  # type: ignore
