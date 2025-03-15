

from dataclasses import dataclass
from uuid import UUID

from core.category.domain.category_repository import CategoryRepository


@dataclass
class ListCategoryRequest:
    pass

@dataclass
class CategoryOutPut:
    id: UUID
    name: str
    description: str
    is_active: bool

@dataclass
class ListCategoryResponse:
    data: list[CategoryOutPut]


class ListCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: ListCategoryRequest) -> ListCategoryResponse:
        categories = self.repository.list()
        
        a=  ListCategoryResponse(
            data=[
                CategoryOutPut(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_active=category.is_active
                ) for category in categories
            ]
        )

        return a