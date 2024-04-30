from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.schemas.base_schema import Base


class Receipt(Base):
    __tablename__ = 'receipt'

    rec_id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    ord_id = Column(String, nullable=False)
    type = Column(String, nullable=False)
    customer_info = Column(String, nullable=False)
    create_date = Column(String, nullable=False)
    rec = Column(String, nullable=False)
