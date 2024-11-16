import uvicorn
from src import config
from src.app.app import app


def run_server():
    uvicorn.run(
        app,
        host=config.BASE_CONFIG["MLServer"]["host"],
        port=int(config.BASE_CONFIG["MLServer"]["port"])
    )


if __name__ == "__main__":
    run_server()