from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from ..deps import get_db
from ..models import Ticket
from ..security import require_api_key

router = APIRouter(
    prefix="/api/v1/reports",
    tags=["reports"],
    dependencies=[Depends(require_api_key)],
)


@router.get("/summary")
def tickets_summary(db: Session = Depends(get_db)):
    total = db.execute(select(func.count()).select_from(Ticket)).scalar_one()

    by_status_rows = db.execute(
        select(Ticket.status, func.count()).group_by(Ticket.status)
    ).all()

    by_status = {status: count for status, count in by_status_rows}

    return {"total": total, "by_status": by_status}
