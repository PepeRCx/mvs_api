from fastapi import APIRouter
from .routes import orders, reports

router = APIRouter()

router.include_router(orders.router, prefix="/orders", tags=["orders"])
router.include_router(reports.router, prefix="/reports", tags=["reports"])
