FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update \
    && apt-get install -y build-essential gettext libpq-dev\
    && apt-get install -y wkhtmltopdf\
    && apt-get install -y gdal-bin\
    && apt-get install -y libgdal-dev\
    && apt-get install -y --no-install-recommends software-properties-common\
    && apt-add-repository contrib\
    && apt-get update

RUN pip install --no-cache-dir -U pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV C_FORCE_ROOT=1

COPY . /code
RUN rm -rf .git
WORKDIR /code