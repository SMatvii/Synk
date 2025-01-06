import uvicorn
from backend import app,migrate


if __name__ == "__main__":
    migrate()
    uvicorn.run(app,port=8080)