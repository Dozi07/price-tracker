from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.dependencies import get_db, get_current_user
from schemas.notification import NotificationOut
from crud.notification import get_user_notifications, mark_as_read, mark_all_as_read

router = APIRouter(tags=["Notifications"])

@router.get("/notifications", response_model=List[NotificationOut])
def fetch_notifications(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return get_user_notifications(db, user_id=current_user.id)


@router.post("/notifications/read")
def read_all_notifications(db: Session = Depends(get_db), current_user = Depends(get_current_user)):

    mark_all_as_read(db, user_id=current_user.id)
    return {"detail": "Все уведомления помечены как прочитанные"}

@router.patch("/notifications/{notification_id}/read")
def read_notification(notification_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):

    success = mark_as_read(db, notification_id=notification_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Уведомление не найдено")
    return {"detail": "Уведомление прочитано"}