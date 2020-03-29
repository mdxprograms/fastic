FROM python:3.7-slim

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

COPY ./Pipfile /app/Pipfile
COPY ./Pipfile.lock /app/Pipfile.lock

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc

RUN pip install pipenv
RUN pipenv install --dev

COPY . /app

# Run fastic
ENTRYPOINT ["pipenv", "run"]

CMD ["python", "fastic.py"]
