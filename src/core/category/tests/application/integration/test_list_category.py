from src.core.category.domain.category import Category
from src.core.category.application.use_cases.list_category import CategoryOutPut, ListCategory, ListCategoryRequest, ListCategoryResponse
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestListCategory:
    def test_return_empty_list(self):
        repository = InMemoryCategoryRepository(categories=[])

        use_case = ListCategory(repository=repository)

        request = ListCategoryRequest()

        response = use_case.execute(request)

        assert response == ListCategoryResponse(data=[])

    def test_return_existing_categories(self):
        category_movie = Category(name="Movie")
        category_tv_show = Category(name="TV Show")

        repository = InMemoryCategoryRepository(
            categories=[category_movie, category_tv_show]
        )

        use_case = ListCategory(repository=repository)

        request = ListCategoryRequest()

        response = use_case.execute(request)

        assert response == ListCategoryResponse(
            data=[CategoryOutPut(
                id=category_movie.id,
                name=category_movie.name,
                description=category_movie.description,
                is_active=True
            ),
            CategoryOutPut(
                id=category_tv_show.id,
                name=category_tv_show.name,
                description=category_tv_show.description,
                is_active=True  
            )]
        )