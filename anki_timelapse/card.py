class Card:
    """Abstraction for the card in the anki database
    """

    def __init__(self, id, deck_id, note_id):
        self.__id = id
        self.__deck_id = deck_id
        self.__note_id = note_id

    @property
    def id(self):
        return self.__id

    @property
    def deck_id(self):
        return self.__deck_id

    @property
    def note_id(self):
        return self.__note_id
