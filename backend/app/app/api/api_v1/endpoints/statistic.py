from app.api.base import BaseHandler # noqa
from app.db.utils import session_scope, model_to_dict # noqa
from app import crud, models, schemas # noqa


class StatisticView(BaseHandler):
    def get(self):
        with session_scope() as db:
            duplicate_elements = crud.msg.get_duplicate_elements(db=db)
            single_elements = crud.msg.get_single_elements(db=db)

            duplicate_counter_sum = sum([el.counter for el in duplicate_elements]) if duplicate_elements else 0
            single_counter_sum = sum([el.counter for el in single_elements]) if single_elements else 0

        total = duplicate_counter_sum + single_counter_sum

        duplicate_percent = duplicate_counter_sum / total if total else 0
        return self.write(
            {
                "percent": int(round(duplicate_percent, 2) * 100)
            }
        )
