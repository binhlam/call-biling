FROM python:3.9-slim

EXPOSE 8001

WORKDIR /app

# Install dependencies
RUN set -x; \
        apt-get update \
        && apt-get install -y --no-install-recommends \
            curl \
            dirmngr \
            git \
            libpq-dev \
            python-dev \
            gcc-aarch64-linux-gnu \
            g++ \
            locales

ENV TZ=Asia/Bangkok
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ADD requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

ENV PYTHONUNBUFFERED 1
ENV FLASK_DEBUG 1
ENV DB_HOST ec2-3-211-6-217.compute-1.amazonaws.com
ENV DB_NAME d5u0mpig7oejaj
ENV DB_USER kebeokwxwpjyeo
ENV DB_PASSWORD bd4b9fe601be36d31dbc9052633647e3313da5c8faef4847a3f82af07e8e5f4e

CMD [ "gunicorn", "--timeout", "3000", "--bind", "0.0.0.0:8001", "main:run()" ]
