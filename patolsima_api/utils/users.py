from django.contrib.auth.models import User
from typing import Iterable


def check_user_is_in_group(user: User, group_name: str) -> bool:
    return user.groups.filter(name=group_name).exists()


def check_user_is_in_all_groups(user: User, group_names: Iterable[str]) -> bool:
    group_names = set(group_names)
    return user.groups.filter(name__in=group_names).count() == len(group_names)


def check_user_is_in_any_group(user: User, group_names: Iterable[str]) -> bool:
    return user.groups.filter(name__in=group_names).exists()
