import uuid


class Category:
    def __init__(
        self, 
        name, 
        id = "", 
        description = "", 
        is_active = True
    ):
        self.id = id or uuid.uuid4()
        self.name = name
        self.description = description
        self.is_active = is_active

        if len(self.name) > 255:
            raise ValueError("name must have less than 255 characters")

    def __str__(self) -> str:
        return f"{self.name} - {self.description} - {self.is_active}"
    
    def __repr__(self) -> str:
        return f"<Category {self.name}>"
    
    def update_category(self, name, description):
        self.name = name
        self.description = description

        if len(self.name) > 255:
            raise ValueError("name must have less than 255 characters")