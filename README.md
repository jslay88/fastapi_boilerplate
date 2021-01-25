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


## Getting Started
Clone the repo to a project dir.
Optionally, remove `remote origin` and add your remote origin, or other name for your remote.

    git clone https://github.com/jslay88/fastapi_boilerplate my_project
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

## Linting
flake8 is already included in `requirements.txt`.
All you have to do to lint is run `flake8` within your venv.

## Coverage
Coverage.py and pytest are already included in `requirements.txt`
Use the following commands to run testing and generate coverage report.

    coverage run -m pytest
    coverage report -m

For more information on generating reports (such as HTML, XML, etc...), go
[here](https://coverage.readthedocs.io/en/coverage-5.2/cmd.html#reporting)

### Current Coverage Report
    ========================= test session starts ==========================
    collected 8 items                                                                                                                               
    
    test\test_unit.py ......
    test\api_v1\test_api_v1.py ..
    ========================== 8 passed in 0.16s ===========================


    Name                                       Stmts   Miss  Cover   Missing
    ------------------------------------------------------------------------
    app\__init__.py                               21      0   100%
    app\api_v1\__init__.py                         9      0   100%
    app\api_v1\model\__init__.py                   2      0   100%
    app\api_v1\model\endpoints.py                 10      0   100%
    app\api_v1\model\example\__init__.py           2      0   100%
    app\api_v1\model\example\endpoints.py         10      0   100%
    app\api_v1\model\example\models.py             7      0   100%
    app\api_v1\model\models.py                     9      0   100%
    app\middleware\__init__.py                     0      0   100%
    app\middleware\correlation_request_id.py      27      0   100%
    app\middleware\logging.py                     29      0   100%
    app\utils\__init__.py                          0      0   100%
    app\utils\auth.py                             28      0   100%
    app\utils\log\__init__.py                      0      0   100%
    app\utils\log\filters.py                      12      0   100%
    app\utils\log\formatters.py                   11      0   100%
    ------------------------------------------------------------------------
    TOTAL                                        177      0   100%

## Loose Ends
### Auth and Tokens
You really do not want to put any sort of token within the code itself.
Ideally, you would read some file from disk that is either mounted to 
the container or downloaded with the `prestart.sh` script and 
register your tokens using `APITokens.regsiter_token` from `app.utils.auth` 
within `app.create_app`. 

This has purposefully been left this way to make you understand the simplicity 
being used here, and up to you to improve upon, or replace this method all together.

More information around Security with FastAPI can be found 
[here](https://fastapi.tiangolo.com/tutorial/security/).
