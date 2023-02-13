from django.contrib.auth.models import User, Group


def perform_destory_from_user_group(group_name: str, user: User):
    group = Group.objects.get(name=group_name)
    if group.user_set.filter(username=user.username, email=user.email).exists():
        group.user_set.remove(user)
        return True
    else:
        return False
