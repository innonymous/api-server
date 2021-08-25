FROM python:3.9

# Environment.
WORKDIR /app
COPY ./requirements.txt /tmp/requirements.txt
RUN python -m venv env && \
    ./env/bin/python -m pip install --no-cache-dir --upgrade pip setuptools wheel && \
    ./env/bin/python -m pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

# Actually, we do not need root.
RUN groupadd innonymous && useradd innonymous -g innonymous

# App.
COPY ./config ./config
COPY ./innonymous ./innonymous

# Run.
USER innonymous
EXPOSE 8000
ENTRYPOINT ["./env/bin/uvicorn", "innonymous.api:app", \
            "--host", "0.0.0.0", \
            "--log-config", "./config/logging.yml"]
