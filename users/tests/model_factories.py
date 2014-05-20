import factory

from django.contrib.auth.models import User
from django.utils import timezone

from projects.tests.model_factories import ProjectF
from dataviews.tests.model_factories import ViewFactory

from ..models import UserGroup, ViewUserGroup


class UserF(factory.django.DjangoModelFactory):
    FACTORY_FOR = User

    @classmethod
    def _setup_next_sequence(cls):
        try:
            return cls._associated_class.objects.values_list(
                'id', flat=True).order_by('-id')[0] + 1
        except IndexError:
            return 0

    username = factory.Sequence(lambda n: "username%s" % n)
    first_name = factory.Sequence(lambda n: "first_name%s" % n)
    last_name = factory.Sequence(lambda n: "last_name%s" % n)
    email = factory.Sequence(lambda n: "email%s@example.com" % n)
    password = ''
    is_staff = False
    is_active = True
    is_superuser = False

    last_login = timezone.datetime(2000, 1, 1).replace(tzinfo=timezone.utc)
    date_joined = timezone.datetime(1999, 1, 1).replace(
        tzinfo=timezone.utc)

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserF, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user


class UserGroupF(factory.django.DjangoModelFactory):
    FACTORY_FOR = UserGroup

    name = factory.Sequence(lambda n: 'name_%d' % n)
    project = factory.SubFactory(ProjectF)
    can_contribute = True

    @factory.post_generation
    def add_users(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.users.add(user)


class ViewUserGroupFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = ViewUserGroup

    usergroup = factory.SubFactory(UserGroupF)
    view = factory.SubFactory(ViewFactory)
    can_moderate = False
    can_read = False
    can_view = True
