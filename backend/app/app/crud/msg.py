from typing import Optional, List

from app.crud.base import CRUDBase # noqa
from app.db.session import Session # noqa
from app.models import Msg # noqa


class CRUDMsg(CRUDBase):
    def get_element_by_key(self, db: Session, *, key: str) -> Optional[Msg]:
        return db.query(self.model).filter(self.model.key == key).first()

    def get_duplicate_elements(self, db: Session) -> List[Msg]:
        return db.query(self.model).filter(self.model.counter > 1).all()

    def get_single_elements(self, db: Session) -> List[Msg]:
        return db.query(self.model).filter(self.model.counter == 1).all()

crud_msg = CRUDMsg(Msg)
