from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..deps import get_db
from ..models import Ticket
from ..schemas import TicketCreate, TicketRead, TicketUpdate
from ..security import require_api_key
from datetime import datetime
from fastapi import Query
from ..schemas import TicketStatus

router = APIRouter(
    prefix="/api/v1/tickets",
    tags=["tickets"],
    dependencies=[Depends(require_api_key)],
)

@router.post("", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db)):
    ticket = Ticket(title=payload.title, description=payload.description)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


@router.get("", response_model=list[TicketRead])
def list_tickets(
    status: TicketStatus | None = None,
    q: str | None = None,
    created_from: datetime | None = None,
    created_to: datetime | None = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    stmt = select(Ticket)

    if status:
        stmt = stmt.where(Ticket.status == status)

    if q:
        stmt = stmt.where((Ticket.title.contains(q)) | (Ticket.description.contains(q)))

    if created_from:
        stmt = stmt.where(Ticket.created_at >= created_from)

    if created_to:
        stmt = stmt.where(Ticket.created_at <= created_to)

    stmt = stmt.order_by(Ticket.id.desc()).limit(limit).offset(offset)
    return db.execute(stmt).scalars().all()


@router.get("/{ticket_id}", response_model=TicketRead)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.patch("/{ticket_id}", response_model=TicketRead)
def update_ticket(ticket_id: int, payload: TicketUpdate, db: Session = Depends(get_db)):
    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(ticket, k, v)

    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    db.delete(ticket)
    db.commit()
    return None
