import sqlite3
from anki_timelapse.revlog import Revlog
from anki_timelapse.card import Card
from anki_timelapse.note import Note
from datetime import datetime, timedelta
from typing import Tuple


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

    def get_revlogs(self, desc=False, start_timestamp=None, end_timestamp=None):
        """Get all the Revolg instances from the connected database

        Args:
            desc: Sorts the revlogs on id (time) descending
            start_timestamp: The unix timestamp in milliseconds
            end_timestamp: The unix timestamp in milliseconds to include as upper bound in the query

        Returns:
            Generator containing Revlog instances

        Raises:
            AssertionException when no connection with the database is established
        """
        assert self.is_connected()
        cursor = self.__conn.cursor()

        if start_timestamp is None:
            start_timestamp = int(datetime.fromtimestamp(0).timestamp() * 1000)

        if end_timestamp is None:
            end_timestamp = int(datetime.now().timestamp() * 1000)

        start_timestamp = min([start_timestamp, end_timestamp])
        end_timestamp = max([start_timestamp, end_timestamp])

        order_by = 'order by id %s' % ('desc' if desc else 'asc')
        query = '''
        select 
            id,
            cid,
            ease,
            type 
        from revlog 
        where id > ? and id < ? %s''' % order_by

        cursor.execute(query, (start_timestamp, end_timestamp))
        for log in cursor.fetchall():
            yield Revlog(log[0], log[1], log[2], log[3])

    def get_cards(self, card_ids):
        """Gets the cards from the database

        Args:
            card_ids: a list of integer card identifiers

        Returns:
            Generator containing cards that match any of the card_ids
        """
        assert self.is_connected()
        query = 'select id, did, nid from cards where id in (%s)' % str.join(',', [
            '?' for i in card_ids])
        cursor = self.__conn.execute(query, card_ids)
        for card in cursor.fetchall():
            yield Card(card[0], card[1], card[2])

    def get_notes(self, note_ids):
        """Get notes from the anki collection

        Args:
            node_ids: a list of note identifiers

        Returns:
            Generator containing notes that match any of the note_ids
        """
        assert self.is_connected()
        query = 'select id, flds from notes where id in (%s)' % str.join(',', [
            '?' for i in note_ids])
        cursor = self.__conn.execute(query, note_ids)
        for note in cursor.fetchall():
            yield Note(note[0], note[1])

    def __exit__(self, type, value, traceback):
        if not self.__conn is None:
            self.__conn.close()
