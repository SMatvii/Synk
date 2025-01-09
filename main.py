from backend import app, migrate
import uvicorn

if __name__ == "__main__":
    migrate()
    uvicorn.run(app,port=8080)


