from unittest.mock import MagicMock
from uuid import UUID
import pytest

from core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import InvalidCategoryData
from src.core.category.application.use_cases.create_category import CreateCategory, CreateCategoryRequest

class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        mock_repository = MagicMock(CategoryRepository)

        use_case = CreateCategory(repository=mock_repository)
        request = CreateCategoryRequest(name="Filme", description="Categoria filmes", is_active=False)
        
        category_id = use_case.execute(request)

        assert category_id is not None
        assert isinstance(category_id.id, UUID)
        assert mock_repository.save.call_count == 1

    def test_create_category_with_invalid_data(self):

        mock_repository = MagicMock(CategoryRepository)

        use_case = CreateCategory(repository=mock_repository)
        request = CreateCategoryRequest(name="")

        with pytest.raises(InvalidCategoryData) as err:
            use_case.execute(request)

        assert err.type == InvalidCategoryData
        assert str(err.value.args[0]) == "name is required"
