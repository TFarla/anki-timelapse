from datetime import datetime, timedelta
from anki_timelapse.database import Database

filepath = '/Users/thomasfarla/Library/Application Support/Anki2/User 1/collection.anki2'
with Database(filepath) as db:
    day_before_yesterday = int(
        (datetime.now() - timedelta(days=2)).timestamp() * 1000)
    g = db.get_revlogs(start_timestamp=day_before_yesterday)
    card_ids = set()
    note_ids = set()
    for log in g:
        card_ids.add(log.card_id)

    cards = db.get_cards(list(card_ids))
    for card in cards:
        note_ids.add(card.note_id)
        print('Card %s' % card.id)
    
    notes = db.get_notes(list(note_ids))
    for note in notes:
        print('Note %s' % note.id)
