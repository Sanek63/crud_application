from app.api.base_handler import BaseHandler # noqa
from app.db.utils import session_scope, model_to_dict # noqa
from app import crud, models, schemas # noqa


class StatisticView(BaseHandler):
    def get(self):
        with session_scope() as db:
            duplicate_counter_sum = crud.msg.get_duplicate_counter_sum(db=db)
            single_counter_sum = crud.msg.get_single_counter_sum(db=db)

        total = duplicate_counter_sum + single_counter_sum

        duplicate_percent = duplicate_counter_sum / total if total > 0 else 0
        return self.write(
            {
                "percent": int(round(duplicate_percent, 2) * 100)
            }
        )
