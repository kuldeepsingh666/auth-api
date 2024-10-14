from fastapi import FastAPI
from .routes import router


def create_app() -> FastAPI:
    """
    Function to create a FastAPI app instance.
    This can be reused to create instances in different environments.
    """
    app = FastAPI()
    app.include_router(router)
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
