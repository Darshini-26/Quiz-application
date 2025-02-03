from fastapi import FastAPI
from router.category import router as category_router
from router.question import router as question_router
from router.auth import router as auth_router
from router.answer import router as answer_router
from router.rating import router as rating_router

app = FastAPI()

app.include_router(category_router)
app.include_router(question_router)
app.include_router(auth_router)
app.include_router(answer_router)
app.include_router(rating_router)