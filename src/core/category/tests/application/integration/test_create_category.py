from uuid import UUID
import pytest
from src.core.category.application.exceptions import InvalidCategoryData
from src.core.category.application.create_category import CreateCategory, CreateCategoryRequest
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        repository = InMemoryCategoryRepository()

        use_case = CreateCategory(repository=repository)
        request = CreateCategoryRequest(name="Filme", description="Categoria filmes", is_active=False)
        
        category_id = use_case.execute(request)

        assert category_id is not None
        assert isinstance(category_id, UUID)
        assert len(repository.categories) == 1

        category = repository.categories[0]
        assert category.name == "Filme"
        assert category.description == "Categoria filmes"
        assert category.is_active is False

    def test_create_category_with_invalid_data(self):
        repository = InMemoryCategoryRepository()

        use_case = CreateCategory(repository=repository)
        request = CreateCategoryRequest(name="")

        with pytest.raises(InvalidCategoryData) as err:
            use_case.execute(request)

        assert err.type == InvalidCategoryData
        assert str(err.value.args[0]) == "name is required"