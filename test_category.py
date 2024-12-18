import uuid
import pytest
from category import Category

class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            Category()

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name must have less than 255 characters"):
            Category("a" * 256)

    def test_category_must_be_create_with_id_as_uuid(self):
        category = Category(name="name")
        assert isinstance(category.id, uuid.UUID)

    def test_created_category_with_default_values(self):
        category = Category(name="name")
        assert category.name == "name"
        assert category.description == ""
        assert category.is_active is True

    def test_category_is_created_as_active_by_default(self):
        category = Category(name="name")
        assert category.is_active is True

    def test_category_is_creted_with_provided_values(self):
        category_id = uuid.uuid4()
        category = Category(
            name="name",
            id=category_id,
            description="description",
            is_active=False
        )
        assert category.id == category_id
        assert category.name == "name"
        assert category.description == "description"
        assert category.is_active is False
            