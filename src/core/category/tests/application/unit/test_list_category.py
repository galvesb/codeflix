from unittest.mock import create_autospec
from src.core.category.application.use_cases.list_category import CategoryOutPut, ListCategory, ListCategoryRequest, ListCategoryResponse
from core.category.domain.category_repository import CategoryRepository
from src.core.category.domain.category import Category


class TestListCategory:
    def test_when_no_categories_in_repository_then_return_empty_list(self):
        mock_repository = create_autospec(CategoryRepository)

        mock_repository.list.return_value = []

        use_case = ListCategory(repository=mock_repository)

        request = ListCategoryRequest()

        response = use_case.execute(request)

        assert response == ListCategoryResponse(data=[])

    def test_when_categories_in_repository_then_return_list(self):
        category_movie  = Category(name="Filme", description="Categoria filmes", is_active=True)
        category_serie = Category(name="Série", description="Categoria séries", is_active=False)

        mock_repository = create_autospec(CategoryRepository)

        mock_repository.list.return_value = [category_movie, category_serie]

        use_case = ListCategory(repository=mock_repository)

        request = ListCategoryRequest()

        response = use_case.execute(request)

        assert response == ListCategoryResponse(
            data=[CategoryOutPut(
                id=category_movie.id,
                name=category_movie.name,
                description=category_movie.description,
                is_active=category_movie.is_active
            ),
            CategoryOutPut(
                id=category_serie.id,
                name=category_serie.name,
                description=category_serie.description,
                is_active=category_serie.is_active
            )]  
        )
        