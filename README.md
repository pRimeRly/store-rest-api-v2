# Stores REST API

### STEPS FOR RUNNING THE APPLICATION LOCALLY
The application should be run with the docker file included

1. Open the project root folder in your IDE of choice.
2. Install dependencies in the `requirements.txt` in your virtual environment.
3. Ensure IDE is using created virtual environment.
4. Open a terminal or command prompt in the directory and run the following command to build the Docker image
```
docker build -t docker-image-tag .
```
5. use the command below to start a container using the docker image and sync the container with the development directory.
```
docker run -dp 5005:5000 -w /app -v "%cd%:/app" flask-smorest-api
```

### Live API 
Visit [URL](https://store-rest-api-v2-project.onrender.com/swagger-ui) below for the live UI documentation and test API endpoints.
