class Revlog:
    __id = None
    __card_id = None
    __ease = None
    __type = None

    def __init__(self, id, card_id, ease, type):
        self.__id = id
        self.__card_id = card_id
        self.__ease = ease
        self.__type = type

    @property
    def id(self):
        return self.__id

    @property
    def card_id(self):
        return self.__card_id

    @property
    def ease(self):
        return self.__ease

    @property
    def type(self):
        return self.__type
