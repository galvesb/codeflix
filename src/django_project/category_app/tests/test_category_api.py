from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from src.core.category.domain.category import Category

from src.django_project.category_app.repository import DjangoORMCategoryRepository


@pytest.fixture
def category_movie():
    return  Category(
        name="Movie",
        description="Movie description",
    )

@pytest.fixture
def category_documentary():
    return Category(
        name="Documentary",
        description="Documentary description",
    )

@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.mark.django_db
class TestCategoryAPI:
    def test_list_categories(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        url = '/api/categories/'
        response = APIClient().get(url)

        expected_data = {"data": [
            {
                "id": str(category_movie.id),
                "name": "Movie",
                "description": "Movie description",
                "is_active": True
            },
            {
                "id": str(category_documentary.id),
                "name": "Documentary",
                "description": "Documentary description",
                "is_active": True
            }
        ]}

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    
@pytest.mark.django_db
class TestRetrieveCategoryAPI:

    def test_when_id_is_invalid_return_404(self):
        url = f'/api/categories/invalid_id/'
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"detail": "Invalid UUID category with id invalid_id"}



    def test_return_category_when_exists(
            self,
            category_movie: Category,
            category_documentary: Category,
            category_repository: DjangoORMCategoryRepository,
        ):
        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        url = f'/api/categories/{category_documentary.id}/'
        response = APIClient().get(url)

        expected_data = { 
            "data": {
                "id": str(category_documentary.id),
                "name": "Documentary",
                "description": "Documentary description",
                "is_active": True
            }
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_return_404_when_category_not_exists(self):
        url = f'/api/categories/7d2bab9b-80b1-45d9-ae02-bf5145cac122/'
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == {"detail": "Category not found with id 7d2bab9b-80b1-45d9-ae02-bf5145cac122"}