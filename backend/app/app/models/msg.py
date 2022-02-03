import json
from sqlalchemy import Column, Text, Integer, JSON, BigInteger, TIMESTAMP
from sqlalchemy.sql import func

from app.db.base_class import Base # noqa


class Msg(Base):
    id = Column(BigInteger, primary_key=True, index=True, nullable=False)

    key = Column(Text(), nullable=False)
    value = Column(JSON, nullable=False)
    counter = Column(Integer(), default=1, nullable=False)

    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), nullable=False, onupdate=func.current_timestamp())

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'value': json.dumps(
                self.value
            )
        }
