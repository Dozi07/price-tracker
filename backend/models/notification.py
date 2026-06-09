from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.engine import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    product_name = Column(String, nullable=False)
    category_name = Column(String, nullable=False)
    text = Column(String, nullable=False)  # Например: "Цена снизилась на 150₽!"

    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связь с пользователем (опционально, если в модели User добавишь back_populates)
    user = relationship("User")