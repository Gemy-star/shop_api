from django.contrib.auth.models import User, Group


def perform_destory_from_user_group(group_name: str, user: User):
    group = Group.objects.get(name=group_name)
    if group.user_set.filter(username=user.username, email=user.email).exists():
        group.user_set.remove(user)
        return True
    else:
        return False


def is_manager(user: User):
    return (User.objects.filter(
        pk=user.pk, groups__name='Manager').exists())


def is_customer(user: User):
    return (User.objects.filter(
        pk=user.pk, groups=None).exists())


def is_delivery_crew(user: User):
    return (User.objects.filter(
        pk=user.pk, groups__name='Delivery Crew').exists())
