# Document Keyword Analyser

This codebase will analyse a folder of text files, detect keywords and frequences and serve them via an API.

## Setup

```bash
mkvirtualenv --no-site-packages venv/
source venv/bin/activate
```

## Pre-implementation analysis

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
jupyter notebook --notebook-dir notebooks/
```

## Running data pipeline(populates database)

```bash
source venv/bin/activate
pip install -r requirements.txt
flask load_docs
```

## Run Tests

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
python manage.py test
```

## Serve the API

```bash
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

Then go to http://localhost:5000/keywords or http://localhost:5000/keyword/:id

## TODO

* API Tests
* Move anything that requires a search to a FTS engine(postgres or elasticsearc perhaps?)
* Proper API Pipeline would be nice, investigated Luigi - looks awesome but wasted too much time on boilerplate, command.py replaced it.
* Parralelise all the things. Could be multi-processor(esp the doc insertion) or separate queues/lambdas/celery tasks
* Split data processing functions up more
* Take in path/keyword count as args
* More efficient serving of related data

## Assumptions

* Hoping an API is a suitable interface(sorry ran out of time on a nice UI)
* Ignoring case in the keyword search
