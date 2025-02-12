from fastapi import APIRouter
from .question import forward_request
from .use_token import get_use_token
from .chat_token import get_chat_token
from .clean_history import clean_history
from .image import get_image

api_router = APIRouter()

api_router.post("/stream")(forward_request)
api_router.post("/getUseToken")(get_use_token)
api_router.post("/getChatToken")(get_chat_token)
api_router.post("/cleanHistory")(clean_history)
api_router.post("/getImage")(get_image)
