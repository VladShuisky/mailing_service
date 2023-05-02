from fastapi import FastAPI

from api.service import VkFriendingService
from api.db_manager import list
from api.db import VkUsers


#to run app: uvicorn main:app --host 127.0.0.1 --port 80 --reload
app = FastAPI(
    title='vk_friending_service'
)

@app.get('/healthcheck')
async def healthcheck():
    return "successful"

@app.get('/bulk_friendship')
async def bulk_friendship():
    vk = VkFriendingService()
    friends_requests = vk.bulk_friends_request()
    return friends_requests