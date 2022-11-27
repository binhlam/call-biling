FROM python:3.9-slim

EXPOSE 8001

WORKDIR /app

# Install some deps, lessc and less-plugin-clean-css, and wkhtmltopdf
RUN set -x; \
        apt-get update \
        && apt-get install -y --no-install-recommends \
            curl \
            dirmngr \
            git \
            libldap2-dev \
            libsasl2-dev \
            libssl-dev\
            libxml2-dev \
            libxslt-dev \
            libpq-dev \
            node-less \
            python-dev \
            gcc-aarch64-linux-gnu \
            libffi-dev \
            libz-dev \
            libjpeg-dev \
            zlib1g-dev \
            g++ \
            locales

RUN set -x; \
        apt-get install -y --no-install-recommends postgresql-client \
        && apt-get install -y --no-install-recommends postgresql postgresql-contrib

ENV TZ=Asia/Bangkok
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ADD requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

ENV PYTHONUNBUFFERED 1
ENV DB_HOST ec2-3-211-6-217.compute-1.amazonaws.com
ENV DB_NAME d5u0mpig7oejaj
ENV DB_USER kebeokwxwpjyeo
ENV DB_PASSWORD bd4b9fe601be36d31dbc9052633647e3313da5c8faef4847a3f82af07e8e5f4e

CMD [ "gunicorn", "--timeout", "3000", "--bind", "0.0.0.0:8001", "main:run()" ]
