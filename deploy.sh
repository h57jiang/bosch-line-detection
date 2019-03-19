#!/usr/bin/env bash
set -e

echo "create a project folder"
mkdir bosch-line-detection
cp line_detector-1.0.0-py3-none-any.whl bosch-line-detection/
cd bosch-line-detection

echo "create a virtual environment"
python3 -m venv venv
. venv/bin/activate

echo "install line_detector"
pip3 install line_detector-1.0.0-py3-none-any.whl


# enable development mode
export FLASK_APP=line_detector

# initialize the SQLite database
# note that using SQLite will cause data loss every time when server restarted
flask init-db

# use a production WSGI server to run, more options available than waitress
pip3 install waitress

echo "deploy the server"
waitress-serve --call 'line_detector:create_app'