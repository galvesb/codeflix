

import pytest

from core.category.domain.category import Category
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.category_app.models import Category as CategoryModel




@pytest.mark.django_db
class TestSave:
    def test_save_category_in_database(self):
        category = Category(name="name")
        repository = DjangoORMCategoryRepository()

        assert CategoryModel.objects.count() == 0

        repository.save(category)

        assert CategoryModel.objects.count() == 1

        category_in_database = CategoryModel.objects.get(id=category.id)

        assert category_in_database.name == category.name
        assert category_in_database.description == category.description
        assert category_in_database.is_active == category.is_active