import uvicorn
from backend import app, migrate
# from frontend import app


if __name__ == "__main__":
    migrate()
    uvicorn.run(port=8080)
    


# if __name__ == "__main__":
#     app.run(debug=True, port = 5000)  ##### I would run flask, and fastapi would comment