from rest_framework import serializers

class CategorySerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    is_active = serializers.BooleanField()


class ListCategorySerializer(serializers.Serializer):
    data = CategorySerializer(many=True)

class RetrieveCategoryRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class RetrieveCategoryResponseSerializer(serializers.Serializer):
    data = CategorySerializer(source='*')


