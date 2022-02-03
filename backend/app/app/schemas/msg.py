from pydantic import BaseModel
from typing import Optional


class MsgBase(BaseModel):
    key: Optional[str] = None
    value: Optional[dict] = None


class MsgCreate(BaseModel):
    key: str
    value: dict


class MsgDelete(BaseModel):
    key: str


class MsgUpdate(BaseModel):
    value: dict
    key: str


class MsgInDBBase(MsgBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class Msg(MsgInDBBase):
    pass
