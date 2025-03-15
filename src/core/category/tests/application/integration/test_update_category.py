from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.category.domain.category import Category


class Test_UpdateCategory:
    def test_can_update_category_name_and_description(self):
        category = Category(name="name", description="description")
        repository = InMemoryCategoryRepository()
        repository.save(category)

        use_case = UpdateCategory(repository=repository)

        request = UpdateCategoryRequest(
            id=category.id,
            name="new name",
            description="new description"
        )

        use_case.execute(request)

        category_updated = repository.get_by_id(category.id)
        assert category_updated.name == "new name"
        assert category_updated.description == "new description"