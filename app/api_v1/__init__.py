import logging

from fastapi import FastAPI

from .model.endpoints import router as model_router
from .model.example.endpoints import router as model_example_router


logger = logging.getLogger(__name__)


api = FastAPI(title='FastAPI App',
              description='This is <strong>an api</strong> that has <code>code and stuff</code> you know?',
              version='1.0.0',
              docs_url='/')


tags_metadata = [
    {
        'name': 'API Helpers'
    },
    {
        'name': 'Example',
        'description': 'This is a description for the namespace, not sure where it renders though'
    }
]

api.include_router(model_router, prefix='/model', tags=['API Helpers'])
api.include_router(model_example_router, prefix='/model/example', tags=['Example'])
