from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.utils import secure_filename
from flask import current_app as app
import os
from bosch_line_detection import db, model

bp = Blueprint("server", __name__)
allowed_extensions = {'csv'}  # todo: make this parameter configurable


@bp.route('/')
def index():
    return render_template('server/index.html')


@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            if db.file_already_uploaded(file.filename):
                flash('%s has been uploaded before, ' % file.filename +
                      'please change the file name if it contains new data')
                return redirect(request.url)
            else:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                db.insert_new_file(file.filename)
                flash('File uploaded successfully')
                return redirect(request.url)
        else:
            flash('This file extension is not allowed, ' +
                  'please upload file in ' + ','.join(allowed_extensions))
            return redirect(request.url)
    return render_template('server/upload.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


@bp.route('/train/<file>')
def train_file(file):
    return _process_file(file, 'train')


@bp.route('/train', methods=['GET', 'POST'])
def train():
    if request.method == 'POST':
        file = request.form['training_file']
        flash(_process_file(file, 'train'))
        return redirect(request.url)
    return render_template('server/train.html')


def _process_file(file, train_or_predict):
    if not db.file_already_uploaded(file):
        return 'Cannot find the file %s, please upload first' % file
    elif train_or_predict == 'train':
        return model.train(file)
    else:
        return model.predict(file)


@bp.route('/predict/<file>')
def predict_file(file):
    return _process_file(file, 'predict')


@bp.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        file = request.form['prediction_file']
        flash(_process_file(file, 'predict'))
        return redirect(request.url)
    return render_template('server/predict.html')


