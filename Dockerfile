FROM --platform=$BUILDPLATFORM python:3.13-alpine AS builder

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 80
ENTRYPOINT ["python3"]
CMD ["app.py"]
