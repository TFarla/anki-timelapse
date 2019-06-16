from datetime import datetime, timedelta
from anki_timelapse.database import Database
from jinja2 import Template
import imgkit
import os
import shutil


class Record:
    __data = {}

    def add(self, date, log, note, card):
        if not date in self.__data.keys():
            self.__data[date] = {}

        self.__data[date][card.id] = {'log': log, 'note': note, 'card': card}

    @property
    def data(self):
        return self.__data


def get_style(level):
    if level <= 0:
        return 'none'

    ranges = [
        (1, 10, 'bad'),
        (10, 20, 'normal'),
        (20, 30, 'intermediate'),
        (30, 40, 'good'),
        (40, 10000, 'great')
    ]

    for (lower, upper, class_name) in ranges:
        if lower <= level <= upper:
            return class_name


data = []

filepath = '/Users/thomasfarla/Library/Application Support/Anki2/User 1/collection.anki2'
stop = False
record = Record()
lazy_days = 0
first_date = datetime.fromisoformat('2019-05-29')
deck_id = '1559208677359'

if os.path.isdir('frames'):
    shutil.rmtree('frames')

os.mkdir('frames')

with open('template.html') as f:
    template = Template(f.read())

with Database(filepath) as db:
    card_meta = {}
    card_notes = {}

    cards = list(db.get_cards(deck_id=deck_id))
    for card in cards:
        card_meta[card.id] = {'level': 0, 'note': '', 'class': 'none'}
        card_notes[card.note_id] = card.id

    notes = list(db.get_notes([card.note_id for card in cards]))
    for note in notes:
        card_meta[card_notes[note.id]]['note'] = note.fields[1]

    while not stop:
        first_date = first_date + timedelta(days=1)
        date = datetime(
            first_date.year,
            first_date.month,
            first_date.day
        )
        end_date = date + timedelta(days=1)

        s_t = int(date.timestamp() * 1000)
        e_t = int(end_date.timestamp() * 1000)

        rows = db.get_rows(from_timestamp=s_t,
                           end_timestamp=e_t, deck_id=deck_id)

        for (log, card, note) in rows:
            level = log.interval_level
            if level > card_meta[card.id]['level']:
                class_name = get_style(level)
                card_meta[card.id]['level'] = log.interval_level
                card_meta[card.id]['class'] = class_name
            lazy_days = 0
            record.add(str(date.date()), log, note, card)
        else:
            lazy_days = lazy_days + 1
            if lazy_days > 5:
                stop = True

        try:
            frame = max([int(os.path.splitext(f)[0])
                         for f in os.listdir('frames')]) + 1
        except ValueError:
            frame = 0

        if not first_date > datetime.now():
            frame = '{0:0=3d}'.format(frame)
            date = datetime.fromtimestamp(int(log.id / 1000))
            page = template.render(card_meta=card_meta, date=first_date)
            imgkit.from_string(page, 'frames/%s.jpg' % frame)

    
    os.system('ffmpeg -r 8 -i frames/%03d.jpg -vcodec libx264 -y -vf scale=1280:-2 -an video.mp4')
