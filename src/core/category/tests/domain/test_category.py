import uuid
import pytest
from src.core.category.domain.category import Category

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

    def test_cannot_create_category_with_empty_name(self):
        with pytest.raises(ValueError, match="name is required"):
            Category(name="")

class TestUpdateCategory:
    def test_update_category_with_name_and_description(self):
        category = Category(name="name", description="description")
        category.update_category(name="new name", description="new description")
        assert category.name == "new name"
        assert category.description == "new description"

    def test_update_category_with_invalid_name_raise_exception(self):
        category = Category(name="name", description="description")
        with pytest.raises(ValueError, match="name must have less than 255 characters"):
            category.update_category(name="a" * 256, description="description")

    def test_cannot_update_category_with_empty_name(self):
        category = Category(name="name", description="description")
        with pytest.raises(ValueError, match="name is required"):
            category.update_category(name="", description="description")

class TestActivate:
    def test_activate_category(self): 
        category = Category(name="Filme", description="filme em geral", is_active=False)

        assert category.is_active is False

        category.activate()

        assert category.is_active is True

            