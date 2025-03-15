from unittest.mock import create_autospec
import uuid
from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from core.category.domain.category_repository import CategoryRepository
from src.core.category.domain.category import Category


class TestUpdateCategory:
    def test_update_category_name(self):
        mock_category = Category(
            id=uuid.uuid4(),
            name="Movie",
            description="Categoria filmes",
            is_active=True
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = mock_category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=mock_category.id, 
            name="Filme"
        )
        use_case.execute(request)

        assert mock_category == Category(
            id=mock_category.id,
            name="Filme",
            description="Categoria filmes",
            is_active=True
        )
        mock_repository.update.assert_called_once_with(mock_category)
        

    def test_update_category_description(self):
        mock_category = Category(
            id=uuid.uuid4(),
            name="Movie",
            description="Categoria filmes",
            is_active=True
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = mock_category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=mock_category.id, 
            description="Filmes de ação"
        )
        use_case.execute(request)

        assert mock_category == Category(
            id=mock_category.id,
            name="Movie",
            description="Filmes de ação",
            is_active=True
        )
        mock_repository.update.assert_called_once_with(mock_category)

    def test_can_deactivate_category(self):
        mock_category = Category(
            id=uuid.uuid4(),
            name="Movie",
            description="Categoria filmes",
            is_active=True
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = mock_category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=mock_category.id, 
            is_active=False
        )
        use_case.execute(request)

        assert mock_category == Category(
            id=mock_category.id,
            name="Movie",
            description="Categoria filmes",
            is_active=False
        )
        mock_repository.update.assert_called_once_with(mock_category)

    def test_can_activate_category(self):
        mock_category = Category(
            id=uuid.uuid4(),
            name="Movie",
            description="Categoria filmes",
            is_active=False
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = mock_category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=mock_category.id, 
            is_active=True
        )
        use_case.execute(request)

        assert mock_category == Category(
            id=mock_category.id,
            name="Movie",
            description="Categoria filmes",
            is_active=True
        )
        mock_repository.update.assert_called_once_with(mock_category)




    