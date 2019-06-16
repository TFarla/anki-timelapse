Transform progress in Anki into a timelapse video

<video controls="" autoplay="" muted="" loop="">
    <source src="https://tfarla.github.io/kanji/video.mp4">
</video>

**Note**: This project will not work out of the box on your machine.
It's been developed to mainly work on one machine, my machine. If you are interested in generating fancy anki timelapses. Please contact me by making an issue on this repository. I will only make this repository reusable when people are interested. 

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
