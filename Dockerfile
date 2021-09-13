ARG PYTHON_VERSION=3.7

# Build dependencies in separate container
FROM tiangolo/uvicorn-gunicorn:python${PYTHON_VERSION} AS builder
ENV WORKDIR /app
COPY Pipfile ${WORKDIR}/
COPY Pipfile.lock ${WORKDIR}/

RUN cd ${WORKDIR} \
    && python -m pip install -U pip setuptools wheel \
    && pip install pipenv \
    && pipenv install --system

# Create the final container with the app
FROM tiangolo/uvicorn-gunicorn:python${PYTHON_VERSION}

ENV HOME=/app \
    PYTHONUNBUFFERED=1
WORKDIR ${HOME}

COPY --from=builder /usr/local/lib/python3.7/site-packages /usr/local/lib/python3.7/site-packages
RUN echo python manage.py migrate >> prestart.sh
COPY . .
RUN python manage.py collectstatic --noinput

ENV APP_MODULE=config.asgi:application