Transform progress in Anki into a timelapse video

# How does it work
This project opens the `collection.anki2` file and queries the `revlog` table which contains all reviews that has ever been done in that instance of Anki. This project does not mutate any data inside the `collection.anki2` file.

# Getting started
Make sure [python 3.7](https://www.python.org/downloads/release/python-370/) and [pipenv](https://github.com/pypa/pipenv) are installed on your machine.

```bash
pipenv install
```

# Contributing
Please make sure the code you're contributing is covered by a test

```bash
pipenv install -d
pipenv run pytest --cov=anki-timelapse tests
```
