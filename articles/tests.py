from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.factories import UserFactory
from .factories import ArticleFactory

class ListTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = reverse("v1:articles-create-list")
        ArticleFactory.create_batch(25)

    def test_get_articles_without_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data["articles"]), 20)
        self.assertEqual(response.data["articlesCount"], 25)
        self.assertEqual(response.data["currentPage"], 1)
        self.assertEqual(response.data["nextPageNumber"], 2)
        self.assertIsNone(response.data["previousPageNumber"])

    def test_get_articles_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["articles"]), 20)
        self.assertEqual(response.data["articlesCount"], 25)
        self.assertEqual(response.data["currentPage"], 1)
        self.assertEqual(response.data["nextPageNumber"], 2)
        self.assertIsNone(response.data["previousPageNumber"])

class RetrieveUpdateTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.article = ArticleFactory(title= "This is title of Article",author=self.user)
        self.url = reverse("v1:article-retrieve-update", kwargs={"slug": self.article.slug})
        self.data = {
            "article": {
                "title": "This is title of Article Updated",
                "description": "This is description of Article Updated",
                "body": "This is body of Article Updated. Please read me more!!!",
                "tagList": ["Ruby (Ruby on Rails)", "Python (Django Rest Framework)"]
            }
        }
    
    def test_get_article_without_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = response.data["article"]
        expected_data = self.article
        self.assertEqual(expected_response["title"], expected_data.title)
        self.assertEqual(expected_response["author"]["email"], self.user.email)

    def test_get_article_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = response.data["article"]
        expected_data = self.article
        self.assertEqual(expected_response["title"], expected_data.title)
        self.assertEqual(expected_response["author"]["email"], self.user.email)
    
    def test_update_without_auth(self):
        response = self.client.put(self.url, data=self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_with_auth_permit(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, data=self.data, format="json")
        expected_response = response.data["article"]
        expected_data = self.data["article"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected_response["title"], expected_data["title"])
        self.assertEqual(expected_response["description"], expected_data["description"])
        self.assertEqual(expected_response["body"], expected_data["body"])
        self.assertEqual(expected_response["tagList"], expected_data["tagList"])
        self.assertEqual(expected_response["author"]["email"], self.user.email)

    def test_update_without_auth_not_permit(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        response = self.client.put(self.url, data=self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class CreateTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = reverse("v1:articles-create-list")
        self.data = {
            "article": {
                "title": "This is title of Article",
                "description": "This is description of Article",
                "body": "This is body of Article. Please read me more",
                "tagList": ["Ruby", "Python"]
            }
        }

    def test_create_without_auth(self):
        response = self.client.post(self.url, data=self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=self.data, format="json")
        expected_response = response.data["article"]
        expected_data = self.data["article"]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(expected_response["title"], expected_data["title"])
        self.assertEqual(expected_response["description"], expected_data["description"])
        self.assertEqual(expected_response["body"], expected_data["body"])
        self.assertEqual(expected_response["tagList"], expected_data["tagList"])
        self.assertEqual(expected_response["author"]["email"], self.user.email)
