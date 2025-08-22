from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from datetime import datetime
from typing import List

from database import get_db

router = APIRouter()


class Item(BaseModel):
    name: str
    price: float


class ItemOut(Item):
    id: int


class OrderCreate(BaseModel):
    customer_name: str
    items: List[Item]


class OrderOut(BaseModel):
    id: int
    customer_name: str
    created_at: str
    items: List[ItemOut]


items = {
    0: Item(name="Hammer", price=9.99, count=20, id=0),
    1: Item(name="Nails", price=1.99, count=100, id=1),
}


@router.post("", response_model=OrderOut)
async def create_order(order: OrderCreate):
    db = await get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO orders (customer_name, created_at) VALUES (?, ?)",
        (order.customer_name, datetime.now().isoformat()),
    )

    order_id = cursor.lastrowid

    for item in order.items:
        cursor.execute(
            "INSERT INTO items (name, price, order_id) VALUES (?, ?, ?)",
            (item.name, item.price, order_id),
        )

    db.commit()

    cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    order_row = cursor.fetchone()
    cursor.execute("SELECT * FROM items WHERE order_id = ?", (order_id,))
    items = [ItemOut(**dict(row)) for row in cursor.fetchall()]

    db.close()
    return OrderOut(
        id=order_row["id"],
        customer_name=order_row["customer_name"],
        created_at=order_row["created_at"],
        items=items,
    )


@router.get("", response_model=List[OrderOut])
async def list_orders(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1)):
    db = await get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM orders LIMIT ? OFFSET ?", (limit, skip))
    orders = cursor.fetchall()

    results = []
    for o in orders:
        cursor.execute("SELECT * FROM items WHERE order_id = ?", (o["id"],))
        items_for_order = [dict(row) for row in cursor.fetchall()]
        items_out_list = [ItemOut(**item) for item in items_for_order]

        order_data = dict(o)
        order_data["items"] = items_out_list

        results.append(OrderOut(**order_data))

    db.close()
    return results


@router.delete("/{order_id}")
async def delete_order(order_id: int):
    db = await get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Order not found")

    cursor.execute("DELETE FROM items WHERE order_id = ?", (order_id,))
    cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))

    db.commit()
    db.close()

    return {"detail": f"Order {order_id} deleted"}
