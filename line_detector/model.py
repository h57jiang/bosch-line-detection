import pandas as pd
import os
import time
from flask import current_app as app
from line_detector import db
from random import randint


def train(filename):
    """Use the file with the filename to train the model.
    This is just a fake train function, to save process time, pandas only read the top 20 rows
    todo: In the real train function, there should be log telling users the process about how much percentage is done
    todo: to accept more file format
    """
    try:
        if filename.rsplit('.', 1)[1].lower() == 'zip':
            pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename), compression='zip', nrows=20)
        else:
            pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename), nrows=20)
        time.sleep(2)
        db.update_file(filename, 'training')
        return 'Training using %s is done' % filename
    except Exception as e:
        return 'Error reading the file %s, details: %s' % (filename, e)


def predict(filename):
    """
    Use the model to predict rows as specified in the file with the filename.
    This is just a fake prediction function, to save process time, pandas only read the top 200 rows, and give
    random (1, 0) to predict the result.
    todo: In the real prediction function, there should be log telling users the process
    todo: to accept more file format
    """
    try:
        dataset = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename), compression='zip', nrows=200) if \
            filename.rsplit('.', 1)[1].lower() == 'zip' \
            else pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename), nrows=200)
        ids = list(dataset.iloc[:, 0].values)
        result = [str(idn) + ',' + str(randint(0, 1)) for idn in ids]
        db.update_file(filename, 'prediction')
        return '<br>'.join(result)
    except Exception as e:
        return 'Error reading the file %s, details: %s' % (filename, e)
