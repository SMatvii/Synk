# Synk

![Synk Logo](frontend/logo/DALL·E%202025-01-23%2010.09.29%20-%20A%20modern%20and%20minimalist%20logo%20design%20for%20a%20web-based%20social%20media%20platform%20named%20'Synk'.%20The%20logo%20should%20prominently%20feature%20the%20word%20'Synk'%20in%20a%20sleek.webp)

**Synk** is a modern social media platform designed for posting, following users, commenting, and community interaction. The backend is built with Python (FastAPI + SQLAlchemy), and the frontend uses Flask (Jinja2), HTML, CSS, and JavaScript.

---

## Features :page_with_curl:

- **Post publication:** create, view, and delete posts.
- **Comments:** add, view, edit, and delete comments on posts.
- **Registration & authentication:** secure registration/login system using JWT (OAuth2).
- **User profiles:** view profile, bio, follower count.
- **Subscriptions:** follow/unfollow users.
- **Search:** search content and users.
- **Light/dark theme:** theme switcher for a comfortable experience.
- **Responsive interface:** modern design, works on all devices.
- **API:** RESTful API for integration and testing (FastAPI).

---

## How to run? :rocket:

1. **Clone the repository**
    ```bash
    git clone https://github.com/SMatvii/Synk.git
    cd Synk
    ```

2. **Install dependencies**
    ```bash
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate for Windows
    ```

3. **Run backend (FastAPI)**
    ```bash
    uvicorn backend:app --reload
    ```
    *Make sure your environment variables (`.env`) are set up*

4. **Run frontend (Flask)**
    ```bash
    cd frontend
    flask run
    ```

5. **Open in your browser**  
   - Backend API: [http://localhost:8000/docs](http://localhost:8000/docs) (interactive Swagger documentation)
   - Frontend: [http://localhost:5000](http://localhost:5000)

---

## Quick Guide

1. **Register/Login**
    - Go to /auth, create an account or log in.
2. **Create a post**
    - After logging in, you can create a new post with a description and content.
3. **Follow users**
    - Open a user's profile and click "Follow".
4. **Comment**
    - Open any post and leave your comment.
5. **Search**
    - Use the search bar in the top menu to find posts/users.
6. **Switch theme**
    - Use the moon/sun icon to toggle interface themes.

---

## Project structure

```
Synk/
├── backend/               # FastAPI backend (API, models, routers)
│   ├── db/
│   ├── routes/
│   └── utils/
├── frontend/              # Flask frontend (templates, static files)
│   ├── templates/
│   └── static/
├── requirements.txt
├── README.md
└── ...
```

---

## Testing

Unit tests for the main features (e.g., CRUD for comments, posts) can be found in their respective test files, such as: `comment_test.py`. To run:
```bash
python -m unittest comment_test.py
```
