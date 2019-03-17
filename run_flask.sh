#!/usr/bin/env bash
set -e

# activate the corresponding environment before working on the project
. venv/bin/activate

# enable development mode
export FLASK_APP=bosch_line_detection
export FLASK_ENV=development

# initialize the SQLite database
# note that using SQLite will cause data loss every time when server restarted
flask init-db

# run flask server
flask run