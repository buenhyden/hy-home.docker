FROM python:3.12-slim-bookworm

# Pins live in requirements.txt, the single file Renovate updates.
COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY hyhome-gx.py /usr/local/bin/hyhome-gx

USER 1000:1000

ENTRYPOINT ["python3", "/usr/local/bin/hyhome-gx"]
