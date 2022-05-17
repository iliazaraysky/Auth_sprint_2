FROM python:3.9-slim-buster
RUN mkdir /app
COPY ./requirements.txt /app
RUN pip install --upgrade pip && pip install -r ../app/requirements.txt
COPY . /app
WORKDIR /app
CMD ["gunicorn", "wsgi_app:app", "--bind", ":5000"]
