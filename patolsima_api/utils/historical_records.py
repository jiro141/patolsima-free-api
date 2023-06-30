from django.contrib.auth.models import User
from typing import Iterable, Dict, Any


def get_history_of_instance(instance) -> Iterable[Dict[str, Any]]:
    if not hasattr(instance, "history"):
        raise ValueError("Model instance does not implement HistoricalRecord manager")

    return [
        {
            "history_id": historical_record.history_id,
            "history_date": historical_record.history_date.isoformat(),
            "history_user": User.objects.get(
                id=historical_record.history_user_id
            ).get_username(),
            "history_type": historical_record.history_type,
            "history_change_reason": historical_record.history_change_reason,
        }
        for historical_record in instance.history.all().order_by("-history_date")
    ]
