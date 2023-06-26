from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from patolsima_api.apps.core.models import Patologo
from patolsima_api.utils.users import check_user_is_in_group


def check_user_is_patologo(user: User) -> Patologo:
    if not check_user_is_in_group(user, "patologo"):
        raise ValidationError(f"{user} can not create Informes.")

    patologo = Patologo.objects.filter(user=user).first()
    if not patologo:
        raise ValidationError(
            f"{user} is in 'patologo' group but does not have a record as Patologo in the system."
        )

    return patologo
