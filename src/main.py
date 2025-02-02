from fastapi import FastAPI
from config.database import Base, engine
from router.user_router import user_router
from router.quiz_router import quiz_router
from router.question_router import question_router
from router.answer_router import answer_router
from router.auth_router import router as auth_router
from router.review_router import  review_router
from router.download_router import router as download_router
from router.s3_router import router as s3_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
# app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(quiz_router, prefix="/quizzes", tags=["Quizzes"])
app.include_router(question_router, prefix="/questions", tags=["Questions"])
app.include_router(answer_router, prefix="/answers", tags=["Answers"])
app.include_router(auth_router, prefix="/authentication", tags=["Authentication"])
app.include_router(review_router, prefix="/Review", tags=["Review"])
app.include_router(download_router, prefix="/Download", tags=["Download"])
# app.include_router(s3_router, prefix="/s3", tags=["s3"])
