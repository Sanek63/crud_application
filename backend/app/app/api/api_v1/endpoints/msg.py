import json

from tornado.routing import PathMatches

from app.api.base_handler import BaseHandler # noqa
from app.api.utils import dict_to_b64 # noqa
from app.db.utils import session_scope, model_to_dict # noqa
from app import crud, models, schemas # noqa

from pydantic import ValidationError

class MethodAndPathMatch(PathMatches):
    def __init__(self, method, path_pattern):
        super().__init__(path_pattern)
        self.method = method

    def match(self, request):
        if request.method != self.method:
            return None

        return super().match(request)


class MsgView(BaseHandler):
    def get(self):
        key_value = self.get_argument('key', default=None, strip=False)
        if not key_value:
            self.set_status(400)
            return self.finish(
                {'detail': 'Invalid key param'}
            )
        with session_scope() as db:
            db_obj = crud.msg.get_element_by_key(db=db, key=key_value)
            if not db_obj:
                self.set_status(400)
                return self.write(
                    {'detail': 'Object not found'}
                )

            self.set_status(200)
            return self.write(
                {
                    "body": {
                        **db_obj.value,
                        'duplicates': db_obj.counter
                    }
                }
            )

    def post(self):
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            json_args = json.loads(self.request.body)
        else:
            json_args = {}

        if not json_args:
            self.set_status(400)
            return self.finish(
                {'detail': 'Body is empty'}
            )

        encode_data = dict_to_b64(dict_in=json_args)
        with session_scope() as db:
            db_obj = crud.msg.get_element_by_key(db=db, key=encode_data)
            if db_obj:
                crud.msg.update(
                    db=db,
                    db_obj=db_obj,
                    obj_in={
                        'counter': db_obj.counter + 1
                    }
                )
            else:
                try:
                    obj_in = schemas.MsgCreate(
                        key=encode_data,
                        value=json_args
                    )
                    crud.msg.create(db=db, obj_in=obj_in)
                except ValidationError as e:
                    self.set_status(400)
                    return self.write(e.json())

            self.set_status(200)
            return self.write(
                {'key': encode_data}
            )

    def put(self):
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            json_args = json.loads(self.request.body)
        else:
            json_args = {}

        try:
            obj_in = schemas.MsgUpdate(**json_args)
        except ValidationError as e:
            self.set_status(400)
            return self.write(e.json())

        key = obj_in.key
        value = obj_in.value

        with session_scope() as db:
            db_obj = crud.msg.get_element_by_key(
                db=db, key=key
            )
            if not db_obj:
                self.set_status(400)
                return self.write(
                    {'detail': 'Object not found'}
                )

            encode_data = dict_to_b64(
                dict_in=value
            )

            crud.msg.update(
                db=db,
                db_obj=db_obj,
                obj_in={
                    'value': value,
                    'key': encode_data,
                    'counter': 1
                }
            )

            self.set_status(200)
            return self.write(
                {'key': encode_data}
            )

    def delete(self):
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            json_args = json.loads(self.request.body)
        else:
            json_args = {}

        with session_scope() as db:
            try:
                obj_in = schemas.MsgDelete(**json_args)
            except ValidationError as e:
                self.set_status(400)
                return self.write(e.json())

            db_obj = crud.msg.get_element_by_key(db=db, key=obj_in.key)
            if not db_obj:
                self.set_status(400)
                return self.write(
                    {'detail': 'Object not found'}
                )

            crud.msg.remove(db=db, id=db_obj.id)

            self.set_status(204)
            return
