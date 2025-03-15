from dataclasses import dataclass
from uuid import UUID

from src.core.category.application.use_cases.exceptions import CategoryNotFound
from core.category.domain.category_repository import CategoryRepository


@dataclass
class DeleteCategoryRequest:
    id: UUID


class DeleteCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: DeleteCategoryRequest):
        category = self.repository.get_by_id(id=request.id)

        if not category:
            raise CategoryNotFound(f"Category with id {request.id} not found")

        self.repository.delete(category.id)
