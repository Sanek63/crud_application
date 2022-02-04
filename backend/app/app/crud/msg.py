from typing import Optional, List

from app.crud.base import CRUDBase # noqa
from app.db.session import Session # noqa
from app.models import Msg # noqa

from sqlalchemy.sql import func


class CRUDMsg(CRUDBase):
    def get_element_by_key(self, db: Session, *, key: str) -> Optional[Msg]:
        return db.query(self.model).filter(self.model.key == key).first()

    def get_duplicate_elements(self, db: Session) -> List[Msg]:
        return db.query(self.model).filter(self.model.counter > 1).all()

    def get_single_elements(self, db: Session) -> List[Msg]:
        return db.query(self.model).filter(self.model.counter == 1).all()

    def get_duplicate_counter_sum(self, db: Session) -> int:
        counter_sum = db.query(
            func.sum(self.model.counter)
        ).filter(
            self.model.counter > 1
        ).scalar()

        return counter_sum if counter_sum else 0

    def get_single_counter_sum(self, db: Session) -> int:
        counter_sum = db.query(
            func.sum(self.model.counter)
        ).filter(
            self.model.counter == 1
        ).scalar()

        return counter_sum if counter_sum else 0

crud_msg = CRUDMsg(Msg)
