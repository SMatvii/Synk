from unittest import IsolatedAsyncioTestCase, main 
from httpx import AsyncClient, ASGITransport
from os import getenv 
from dotenv import load_dotenv 

from sqlalchemy import select

from backend import app, Config, User, Post, Comment

Session = Config.SESSION

load_dotenv() 
API_URL = getenv("BACKEND_URL") 
 
 
class TestCommentCRUD(IsolatedAsyncioTestCase): 
    async def asyncSetUp(self): 
        self.client = AsyncClient(transport=ASGITransport(app=app),base_url=API_URL) 
 
        user_payload = { 
            "name": "Test User", 
            "email": "testuser@example.com", 
            "password": "password123", 
            "bio": "This is a test user.", 
        } 
        user_response = await self.client.post("users/registrate", json=user_payload) 
        print("User creation response:", user_response.json()) 
        self.assertEqual(user_response.status_code, 201)
        user_name = user_response.json().get("name")
        with Session() as session:
            user = session.scalar(select(User).where(User.name==user_name))
            self.user_id = user.id
        
        login_payload = { 
            "username": "Test User", 
            "password": "password123", 
        } 
 
        login_response = await self.client.post("auth/token", data=login_payload)
        print(login_response.json())
        self.token = login_response.json().get("access_token")

        post_payload = { 
            "title": "Test Post", 
            "content": "This is a test post.", 
            "user_id": self.user_id, 
        } 

        post_response = await self.client.post("/posts/create", json=post_payload, headers={"authorization": f"Bearer {self.token}"}) #  headers={"authorization": f"Bearer {self.token}"}, to make requests to protected endpoints
        print("Post creation response:", post_response.json()) 
        self.assertEqual(post_response.status_code, 201) 
        post_title = post_response.json().get("title")
        with Session() as session:
            post = session.scalar(select(Post).where(Post.title==post_title))
            self.post_id = post.id
 
    async def asyncTearDown(self): 
 
        if hasattr(self, "user_id"): 
            await self.client.delete(f"/users/delete/{self.user_id}") 
        await self.client.aclose() 
 
    async def test_create_comment(self): 
 
        payload = { 
            "content": "This is a test comment.", 
            "post_id": self.post_id, 
            "user_id": self.user_id, 
        } 
        response = await self.client.post("/comments/create", json=payload, headers={"authorization": f"Bearer {self.token}"}) 
        self.assertEqual(response.status_code, 201)  
        comment_content = response.json().get("content")
        with Session() as session:
            comment = session.scalar(select(Comment).where(Comment.content==comment_content))
            self.comment_id = comment.id


if __name__ == "__main__": 
    main()