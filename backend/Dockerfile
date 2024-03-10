FROM python:3.11.4

RUN apt update && apt install -y gettext libgettextpo-dev && pip install --upgrade pip

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

RUN ./setup.sh

CMD ["python", "manage.py", "runsslserver", "192.168.90.2:8080"]