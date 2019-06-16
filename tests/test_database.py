import os
import sqlite3
from anki_timelapse.database import Database
from anki_timelapse.revlog import Revlog

current_dir = os.path.dirname(__file__)

paths = {
    'empty': os.path.join(current_dir, 'fixtures', 'collection.anki2_empty'),
    'with_data': os.path.join(current_dir, 'fixtures', 'collection.anki2_with_data')
}


def test_read_revlog_with_empty_database():
    with Database(paths['empty']) as db:
        logs = db.get_revlogs()
        assert len([log for log in logs]) == 0


def test_read_revlog():
    with Database(':memory:') as db:
        setup_db(db)
        for log in db.get_revlogs():
            assert isinstance(log, Revlog)


def test_read_revlog_order():
    with Database(':memory:') as db:
        setup_db(db)
        revlog_desc = list(db.get_revlogs(desc=True))
        revlog_asc = list(db.get_revlogs())
        assert revlog_asc[0].id == revlog_desc[-1].id
        assert revlog_desc[0].id == revlog_asc[-1].id


def setup_db(db: Database):
    new_db = db._Database__conn
    old_db = sqlite3.connect(paths['with_data'])

    query = ''.join(line for line in old_db.iterdump())
    new_db.executescript(query)
    c = new_db.cursor()
    c.execute('select * from revlog')
    c.fetchall()
