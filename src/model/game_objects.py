from .interface import ICharacter, IRoom


class Character(ICharacter):
    def __init__(self):
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
