from .endpoints import auth, users, laudos, ai_analysis

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(laudos.router, prefix="/laudos", tags=["laudos"])
api_router.include_router(
    ai_analysis.router,
    prefix="/ai",
    tags=["ai-analysis"]
)