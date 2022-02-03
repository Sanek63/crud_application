from typing import TypeVar
from contextlib import contextmanager

from app.db.session import Session # noqa
from app.db.base_class import Base # noqa

ModelType = TypeVar('ModelType', bound=Base)

def model_to_dict(model: ModelType) -> dict:
    obj = {}
    for col in model.__table__.columns:
        obj[col.name] = getattr(model, col.name)

    return obj


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
