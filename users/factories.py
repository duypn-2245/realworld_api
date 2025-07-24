import factory
from .models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("email",)

    email = factory.Faker("email")
    username = factory.Faker("user_name")
    
    def _create(cls, *args, **kwargs):
        password = kwargs.pop("password", "Aa@123456")
        user = User.objects.create(*args, **kwargs)
        user.set_password(password)
        user.save()
        return user
