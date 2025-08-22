from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from database import get_db

router = APIRouter()


@router.get("/sales")
async def total_sales():
    db = await get_db()
    cursor = db.cursor()

    cursor.execute("SELECT SUM(price) as total FROM items")
    total = cursor.fetchone()["total"] or 0

    db.close()
    return {"total_sales": total}


@router.get("/top-products")
async def top_products():
    db = await get_db()
    cursor = db.cursor()

    cursor.execute(
        """
            SELECT name, SUM(price) as total_sales, COUNT(*) as sold_count
            FROM items
            GROUP BY name
            ORDER BY sold_count DESC
            LIMIT 3
        """
    )

    top = [dict(row) for row in cursor.fetchall()]

    db.close()
    return top
