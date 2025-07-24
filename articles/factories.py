import factory
from users.factories import UserFactory
from .models import Article

class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    title = factory.Faker("sentence", nb_words=10)
    description = factory.Faker("paragraph", nb_sentences=1)
    body = factory.Faker("paragraph", nb_sentences=10)
    author = factory.SubFactory(UserFactory)
