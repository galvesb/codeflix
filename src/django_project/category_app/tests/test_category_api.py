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


@pytest.mark.django_db
class TestCreateCategoryAPI:
    def test_when_payload_is_invalid_return_400(self):
        url = '/api/categories/'
        response = APIClient().post(url, {
            "name": "",
            "description": "Description"
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    
    def test_when_payload_is_valid_return_201(self):
        url = '/api/categories/'
        response = APIClient().post(url, {
            "name": "Movie",
            "description": "Description"
        })

        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestUpdateCategoryAPI:
    def test_when_payload_is_invalid_return_400(self):
        url = '/api/categories/7d2bab9b-80b1-45d9-ae02-bf5145cac123/'
        response = APIClient().put(url, {
            "name": "",
            "description": "Description",
            "is_active": True
        },
        format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"name": ["This field may not be blank."]}


    def test_when_payload_is_valid_return_204(
            self,
            category_movie: Category,
            category_repository: DjangoORMCategoryRepository
    ):
        
        category_repository.save(category_movie)

        url = f'/api/categories/{category_movie.id}/'
        response = APIClient().put(url, {
            "name": "Movie1",
            "description": "Description1",
            "is_active": False
        },
        format="json"
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        category_movie = category_repository.get_by_id(category_movie.id)
        assert category_movie.name == "Movie1"
        assert category_movie.description == "Description1"
        assert not category_movie.is_active


@pytest.mark.django_db
class TestDeleteCategoryAPI:

    def test_when_id_is_valid(
            self,
            category_movie: Category,
            category_repository: DjangoORMCategoryRepository
        ):
        category_repository.save(category_movie)

        url = f'/api/categories/{category_movie.id}/'
        response = APIClient().delete(url)
        category_movie = category_repository.get_by_id(category_movie.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert category_movie is None


@pytest.mark.django_db
class TestPartialUpdateAPI:
    @pytest.mark.parametrize(
        "payload,expected_category_dict",
        [
            (
                {
                    "name": "Not Movie",
                },
                {
                    "name": "Not Movie",
                    "description": "Movie description",
                    "is_active": True,
                },
            ),
            (
                {
                    "description": "Another description",
                },
                {
                    "name": "Movie",
                    "description": "Another description",
                    "is_active": True,
                },
            ),
            (
                {
                    "is_active": False,
                },
                {
                    "name": "Movie",
                    "description": "Movie description",
                    "is_active": False,
                },
            ),
        ],
    )
    def test_when_request_data_is_valid_then_update_category(
        self,
        payload: dict,
        expected_category_dict: dict,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(category_movie)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().patch(url, data=payload, format="json")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        updated_category = category_repository.get_by_id(category_movie.id)

        assert updated_category.name == expected_category_dict["name"]
        assert updated_category.description == expected_category_dict["description"]
        assert updated_category.is_active == expected_category_dict["is_active"]


@pytest.mark.django_db
class TestE2ECategoryAPI:
    def test_e2e(self):
         url = '/api/categories/'
         APIClient().post(url, {
            "name": "Movie",
            "description": "Description",
            "is_active": True
         })
         APIClient().post(url, {
            "name": "Documentary",
            "description": "Description",
            "is_active": True
         })

         response = APIClient().get(url)

         assert response.status_code == status.HTTP_200_OK
         assert len(response.data["data"]) == 2
         assert response.data["data"] == [
            {
                "id": response.data["data"][0]["id"],
                "name": "Movie",
                "description": "Description",
                "is_active": True
            },
            {
                "id": response.data["data"][1]["id"],
                "name": "Documentary",
                "description": "Description",
                "is_active": True
            }
         ]

         url = f'/api/categories/{response.data["data"][0]["id"]}/'

         response =APIClient().get(url, format="json")

         assert response.status_code == status.HTTP_200_OK
         assert response.data["data"] == {
            "id": response.data["data"]["id"],
            "name": "Movie",
            "description": "Description",
            "is_active": True
         }

         response = APIClient().put(url, {
            "name": "Movie1",
            "description": "Description1",
            "is_active": False
         },
         format="json"
         )

         assert response.status_code == status.HTTP_204_NO_CONTENT

         response = APIClient().get(url)

         

         assert response.data["data"] == {
            "id": response.data["data"]["id"],
            "name": "Movie1",
            "description": "Description1",
            "is_active": False
         }

         response = APIClient().delete(url)

         assert response.status_code == status.HTTP_204_NO_CONTENT
         
         response = APIClient().get(url)

         assert response.status_code == status.HTTP_404_NOT_FOUND
        
        