class Revlog:
    def __init__(self, id, card_id, ease, type, interval_level):
        self.__id = id
        self.__card_id = card_id
        self.__ease = ease
        self.__type = type
        self.__interval_level = interval_level

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

    @property
    def interval_level(self):
        return self.__interval_level