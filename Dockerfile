FROM python:slim

RUN python -m venv /venv
ENV path="/venv/bin:$PATH"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src /src

WORKDIR /src

# CMD python manage.py runserver 0.0.0.0:8888
CMD gunicorn --bind :8888 superlists.wsgi:application
