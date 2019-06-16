import os
import sqlite3
from anki_timelapse.database import Database
from anki_timelapse.revlog import Revlog
from datetime import datetime
import decorator
import pytest

current_dir = os.path.dirname(__file__)

paths = {
    'empty': os.path.join(current_dir, 'fixtures', 'collection.anki2_empty'),
    'with_data': os.path.join(current_dir, 'fixtures', 'collection.anki2_with_data')
}

card_ids = [1559208810743, 1559208810752]


@pytest.fixture
def db():
    with Database(':memory:') as db:
        setup_db(db, copy_from=paths['with_data'])
        yield db


@pytest.fixture
def empty_db():
    with Database(':memory:') as db:
        setup_db(db, copy_from=paths['empty'])
        yield db


def test_read_revlog_with_empty_database(empty_db: Database):
    logs = empty_db.get_revlogs()
    assert len([log for log in logs]) == 0


def test_read_revlog(db: Database):
    for log in db.get_revlogs():
        assert isinstance(log, Revlog)


def test_read_revlog_order(db: Database):
    revlog_desc = list(db.get_revlogs(desc=True))
    revlog_asc = list(db.get_revlogs())
    assert revlog_asc[0].id == revlog_desc[-1].id
    assert revlog_desc[0].id == revlog_asc[-1].id


def test_read_revlog_for_a_given_day(db: Database):
    start_timestamp = 1560577038325
    end_timestamp = 1560577123969

    logs = db.get_revlogs(
        start_timestamp=start_timestamp, end_timestamp=end_timestamp)
    assert len(list(logs)) == 4


def test_get_cards_on_empty(empty_db: Database):
    card_ids = []
    result = empty_db.get_cards(card_ids)
    assert len(list(result)) == 0


def test_get_cards(db: Database):
    result = db.get_cards(card_ids)
    list_result = list(result)
    assert len(list_result) == len(card_ids)
    found_ids = [card.id for card in list_result]
    for id in card_ids:
        assert id in found_ids


def test_get_notes_from_empty_database(empty_db: Database):
    note_ids = [1, 2, 3]
    result = empty_db.get_notes(note_ids)
    assert len(list(result)) == 0


def test_get_notes(db: Database):
    note_ids = [card.note_id for card in db.get_cards(card_ids)]
    notes = list(db.get_notes(note_ids))
    assert len(notes) == len(note_ids)
    for n in notes:
        assert n.id in note_ids


def setup_db(db: Database, copy_from):
    new_db = db._Database__conn
    old_db = sqlite3.connect(copy_from)

    query = ''.join(line for line in old_db.iterdump())
    new_db.executescript(query)
