from uuid import UUID
import uuid
from dataclasses import dataclass, field

@dataclass
class Category:
    name: str
    description: str = ""
    is_active: bool = True
    id: UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        self.validate()



    def validate(self):
        if len(self.name) > 255:
            raise ValueError("name must have less than 255 characters")
        
        if not self.name:
            raise ValueError("name is required")

    def __str__(self) -> str:
        return f"{self.name} - {self.description} - {self.is_active}"
    
    def __repr__(self) -> str:
        return f"<Category {self.name}>"
    
    def update_category(self, name, description):
        self.name = name
        self.description = description

        self.validate()

    def activate(self):
        self.is_active = True

        self.validate()