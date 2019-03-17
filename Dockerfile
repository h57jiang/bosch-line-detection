FROM python:2-alpine

COPY *.txt setup.py /code/
ADD purge /code/purge/
ADD test /code/test/
WORKDIR /code

RUN find . -name \*.pyc -delete && \
    apk update \ && \
    apk add --virtual build-deps gcc python-dev libffi-dev openssl-dev musl-dev && \
    pip install --upgrade pip && \
    pip install -r requirements-test.txt && \
    pip install -e . /code && \
    apk del build-deps

WORKDIR test

CMD ["pytest"]

FROM python:2-alpine

COPY main.py requirements.txt setup.py config_default.yml /code/
ADD purge /code/purge/
WORKDIR /code

RUN find . -name \*.pyc -delete && \
    apk update \ && \
    apk add --virtual build-deps gcc python-dev libffi-dev openssl-dev musl-dev && \
    pip install --upgrade pip && \
    pip install -e . && \
    apk del build-deps

ENV INTERFACE="0.0.0.0"

ENTRYPOINT python -m flask run --host=${INTERFACE}