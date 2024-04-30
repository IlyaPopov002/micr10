#FROM python:3.10
#
## Выбор папки, в которой будет вестись работа
#WORKDIR /app_receipt
#
## Установка зависимостей проекта
#COPY ./requirements.txt /app_receipt/
#RUN pip install --no-cache-dir --upgrade -r /app_receipt/requirements.txt
#
## Перенос проекта в образ
#COPY ./app /app_receipt/app
#COPY .env /app_receipt
#
## Копирование файлов alembic
#COPY ./migration /app_receipt/migration
#COPY ./alembic.ini /app_receipt/alembic.ini
#
#EXPOSE 8080
#
## Добавляем путь к корневому каталогу проекта в PYTHONPATH
#ENV PYTHONPATH="${PYTHONPATH}:/app_receipt"
#ENV PYTHONPATH="${PYTHONPATH}:/app_receipt/app"
#
#CMD ["/bin/sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8080"]

FROM python:3.10

WORKDIR /app_receipt

# Установка зависимостей проекта
COPY ./requirements.txt /app_receipt/
RUN pip install --no-cache-dir --upgrade -r /app_receipt/requirements.txt

# Перенос проекта в образx
COPY ./app /app_receipt/app
COPY .env /app_receipt

# Копирование файлов alembic
COPY ./migration /app_receipt/migration
COPY ./alembic.ini /app_receipt/alembic.ini

EXPOSE  8080

# Добавляем путь к корневому каталогу проекта в PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:/app_receipt"
ENV PYTHONPATH="${PYTHONPATH}:/app_receipt/app"

CMD ["/bin/sh", "-c", "alembic upgrade head && uvicorn app.main:app --host  0.0.0.0 --port  81"]