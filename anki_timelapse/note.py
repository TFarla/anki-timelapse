class Note:
    """Abstract for the rows in the `notes` table in the anki collection
    """

    def __init__(self, id, fields):
        self.__id = id
        self.__fields = fields

    @property
    def id(self):
        return self.__id

    @property
    def fields(self):
        return self.__fields
    
