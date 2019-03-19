import pandas as pd
import os
import time
from flask import current_app as app
from line_detector import db
from random import randint


def train(filename):
    try:
        pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        time.sleep(2)
        db.update_file(filename, 'training')
        return 'Training using %s is done' % filename
    except Exception as e:
        return 'Error reading the file %s, details: %s' % (filename, e)


def predict(filename):
    try:
        dataset = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        ids = list(dataset.iloc[:, 0].values)
        result = [str(idn) + ',' + str(randint(0, 1)) for idn in ids]
        db.update_file(filename, 'prediction')
        return '<br>'.join(result)
    except Exception as e:
        return 'Error reading the file %s, details: %s' % (filename, e)
