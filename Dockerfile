FROM python:3.9-slim

WORKDIR /app

COPY spotify-to-tidal.py .

RUN pip install --no-cache-dir requests==2.31.0

ENTRYPOINT ["python", "spotify-to-tidal.py"]
