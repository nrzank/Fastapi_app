from fastapi import APIRouter

from .officers.views import router as officer_router
from .departments.views import router as department_router
from .auth.views import router as user_router

router = APIRouter()

router.include_router(router=officer_router,
                      prefix="/officer"
                      )
router.include_router(router=department_router,
                      prefix="/department"
                      )
router.include_router(router=user_router,
                      prefix="/register"
                      )




