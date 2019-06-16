import sqlite3
from anki_timelapse.revlog import Revlog


class Database:
    """Abstraction to interact with the anki database

    Examples:
        >>> with Database(':memory:') as db:
        >>>    revlogs = db.get_revlogs()
    """
    __collection_path = None
    __conn = None

    def __init__(self, collection_path):
        self.__collection_path = collection_path

    def __enter__(self):
        self.__conn = sqlite3.connect(self.__collection_path)
        return self

    def is_connected(self):
        """Returns wether the instance is connected with the database."""
        return not self.__conn is None

    def get_revlogs(self, desc=False):
        """Get all the Revolg instances from the connected database

        Args:
            desc: Sorts the revlogs on id (time) descending
        
        Returns:
            Generator containing Revlog instances
        
        Raises:
            AssertionException when no connection with the database is established
        """
        assert self.is_connected()
        cursor = self.__conn.cursor()
        order_by = 'order by id %s' % ('desc' if desc else 'asc')
        query = 'select id, cid, ease, type from revlog %s' % order_by
        cursor.execute(query)
        for log in cursor.fetchall():
            yield Revlog(log[0], log[1], log[2], log[3])

    def __exit__(self, type, value, traceback):
        if not self.__conn is None:
            self.__conn.close()
