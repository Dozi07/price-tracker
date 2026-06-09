from sqlalchemy.orm import Session
from models.notification import Notification


def create_notification(db: Session, product_name: str, category_name: str, text: str, user_id: int):
    db_notif = Notification(
        user_id=user_id,
        product_name=product_name,
        category_name=category_name,
        text=text
    )
    db.add(db_notif)
    db.commit()
    db.refresh(db_notif)
    return db_notif


def get_user_notifications(db: Session, user_id: int):
    return db.query(Notification)\
        .filter(Notification.user_id == user_id,Notification.is_read == False)\
        .order_by(Notification.created_at.desc())\
        .all()


def mark_as_read(db: Session, notification_id: int, user_id: int):
    db_notif = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == user_id
    ).first()

    if db_notif:
        db_notif.is_read = True
        db.commit()
        db.refresh(db_notif)
        return True
    return False

def mark_all_as_read(db: Session, user_id: int):
    db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.is_read == False
    ).update({"is_read": True}, synchronize_session=False)
    db.commit()