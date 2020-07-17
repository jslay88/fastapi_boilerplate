# FastAPI Boilerplate
A FastAPI application boilerplate built for ML teams.

## Features
* Modular design
* Starter unit tests
* docker-compose.yml for local development
* Production ready Dockerfile
* Basic HTTP Bearer Auth
* JSON Formatter for logging in JSON string
* Pre-Start scripts for downloading/setting up files pre-start


## Getting Starting
Clone the repo, and rename the directory. 
Remove `remote origin` and add your remote origin.

    git clone https://github.com/jslay88/fastapi_boilerplate
    mv fastapi_boilerplate my_project
    cd my_project
    git remote remove origin
    git remote add origin https://github.com/username/repo
    git push -u origin master
    
Use docker-compose to start the application

    docker-compose up --build
    
Docs are available at
    
    http://localhost:8080/api/v1/
    
Default Token (defined in `app/__init__.py`)

    ABCABCABC
