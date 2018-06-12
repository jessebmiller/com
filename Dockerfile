FROM python:alpine

RUN mkdir /workspace
WORKDIR /workspace

RUN pip install pipenv

COPY ./Pipfile ./Pipfile
# COPY ./Pipfile.lock ./Pipfile.lock

RUN pipenv install

COPY . .

VOLUME /out
ENV TARGET_ROOT /out

CMD pipenv run python src/generate.py