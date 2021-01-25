FROM python:3.8-alpine3.10 as base
RUN apk add --no-cache --virtual .build-deps gcc libc-dev make \
    && pip install -U --no-cache-dir uvloop pip setuptools
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN apk del .build-deps

COPY container/prestart.sh /app/prestart.sh
COPY container/start.sh /start.sh
RUN chmod +x /app/prestart.sh
RUN chmod +x /start.sh

COPY gunicorn_conf.py /gunicorn_conf.py

COPY container/start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

FROM base
WORKDIR /app
COPY app /app/app

ENV PYTHONPATH=/app

EXPOSE 80

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["/start.sh"]
