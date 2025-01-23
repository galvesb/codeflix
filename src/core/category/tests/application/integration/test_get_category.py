from src.core.category.application.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.category.domain.category import Category


class TestGetCategory:
    def test_get_category_by_id(self):
        category_movie = Category(name="Movie")
        category_tv_show = Category(name="TV Show")

        repository = InMemoryCategoryRepository(
            categories=[category_movie, category_tv_show]
        )

        use_case = GetCategory(repository=repository)
        
        request = GetCategoryRequest(id=category_movie.id)

        response = use_case.execute(request)

        assert response == GetCategoryResponse(
            id=category_movie.id,
            name=category_movie.name,
            description=category_movie.description,
            is_active=True
        )

    def test_when_category_does_not_exist_then_raise_exception(self):
        category_movie = Category(name="Movie")
        category_tv_show = Category(name="TV Show")

        repository = InMemoryCategoryRepository(
            categories=[category_movie, category_tv_show]
        )