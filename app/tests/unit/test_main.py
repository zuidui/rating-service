from fastapi import FastAPI

from demo.main import app


def test_create_application():
    assert isinstance(app, FastAPI)
