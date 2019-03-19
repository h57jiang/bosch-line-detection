
import io
from line_detector.db import get_db


def test_index(client):
    response = client.get('/')
    assert b"Welcome to Bosch line failure detection" in response.data
    assert b"upload a file" in response.data
    assert b"train a model" in response.data
    assert b"predict using the model" in response.data


def test_upload(client, app):
    file_correct = dict(
        file=(io.BytesIO(b'h1,h2,h3\n1,2,3'), "test1.csv"),
    )
    client.post('/upload', content_type='multipart/form-data', data=file_correct, follow_redirects=True)

    with app.app_context():
        db = get_db()
        post = db.execute("SELECT * FROM files WHERE name = 'test1.csv'").fetchone()
        assert post['name'] == 'test1.csv'

    file_duplicate = dict(
        file=(io.BytesIO(b'h1,h2,h3\n1,2,3'), "test1.csv"),
    )

    response_duplicate = client.post('/upload', content_type='multipart/form-data', data=file_duplicate,
                                     follow_redirects=True)
    assert b"test1.csv has been uploaded before" in response_duplicate.data

    file_wrong_type = dict(
        file=(io.BytesIO(b'h1,h2,h3\n1,2,3'), "test1.txt"),
    )
    response_wrong_type = client.post('/upload', content_type='multipart/form-data', data=file_wrong_type,
                                      follow_redirects=True)
    assert b"This file extension is not allowed" in response_wrong_type.data

    response_file_missing = client.post('/upload', content_type='multipart/form-data', data='', follow_redirects=True)
    assert b"No file part" in response_file_missing.data


def test_train(client):
    # first upload the file
    file1 = dict(
        file=(io.BytesIO(b'h1,h2,h3\n1,2,3'), "test1.csv"),
    )
    client.post('/upload', content_type='multipart/form-data', data=file1)

    assert client.get('/train/test1.csv').status_code == 200

    file2 = dict(
        file=(io.BytesIO(b'h1,h2,h3\n1,2,3'), "test2.csv"),
    )
    client.post('/upload', content_type='multipart/form-data', data=file2)

    response = client.post(
        '/train',
        data={'training_file': 'test2.csv'},
        follow_redirects=True
    )
    assert b"Training using test2.csv is done" in response.data

    response = client.post(
        '/train',
        data={'training_file': 'test4.csv'},
        follow_redirects=True
    )
    assert b"Cannot find the file test4.csv, please upload first" in response.data


def test_predict(client):
    file1 = dict(
        file=(io.BytesIO(b'h1,h2,h3\n1,2,3'), "test1.csv"),
    )
    client.post('/upload', content_type='multipart/form-data', data=file1)

    assert client.get('/predict/test1.csv').status_code == 200

    file2 = dict(
        file=(io.BytesIO(b'h1,h2,h3\na,2,3\nb,3,4'), "test2.csv"),
    )
    client.post('/upload', content_type='multipart/form-data', data=file2)

    assert client.post(
        '/predict',
        data={'prediction_file': 'test2.csv'},
        follow_redirects=True
    ).status_code == 200

    response = client.post(
        '/predict',
        data={'prediction_file': 'test4.csv'},
        follow_redirects=True
    )
    assert b"Cannot find the file test4.csv, please upload first" in response.data

    file3 = dict(
        file=(io.BytesIO(b'h1,h2,h3\nid1,2,3'), "test5.csv"),
    )
    client.post('/upload', content_type='multipart/form-data', data=file3)

    response = client.get('/predict/test5.csv')
    assert b'id1,' in response.data

