FROM python:alpine

RUN mkdir /workspace
WORKDIR /workspace

RUN pip install pipenv

COPY ./Pipfile ./Pipfile
COPY ./Pipfile.lock ./Pipfile.lock

RUN pipenv install --system

COPY . .

VOLUME /out
ENV SITE_ROOT /out

CMD python src/generate.py