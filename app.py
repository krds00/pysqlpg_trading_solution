"""Module for building app for main. build the app with 'uvicorn app:app --host 0.0.0.0 --port 8000'"""

from fastapi import FastAPI
from main import main

app = FastAPI()

@app.get("/run-main")
def run_main() -> dict[str, str]:
    """Run main function
    you can call this function from terminal
    curl -X 'GET' \
    'http://0.0.0.0:8000/run-main' \
    -H 'accept: application/json'
    or got to http://0.0.0.0:8000/run-main
    """
    main()
    return {"message": "Main function executed"}

