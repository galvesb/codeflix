from abc import ABC, abstractmethod


class CategoryRepository(ABC):
    @abstractmethod
    def save(self, category) -> None:
        raise NotImplementedError