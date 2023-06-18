# CONTRIBUTING

## How to build your image

```
docker build -t DOCKER-IMAGE-NAME .
```

## How to run the Dockerfile locally

Windows
```
docker run -dp 5006:5000 -w /app -v "%cd%:/app" DOCKER_IMAGE_NAME sh -c "flask run --host 0.0.0.0"
```

Mac/Linux
```
docker run -dp 5006:5000 -w /app -v "$(pwd):/app" DOCKER_IMAGE_NAME sh -c "flask run --host 0.0.0.0"
```