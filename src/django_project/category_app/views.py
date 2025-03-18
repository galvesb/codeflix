from uuid import UUID
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from src.core.category.application.use_cases.delete_category import DeleteCategory, DeleteCategoryRequest
from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from src.core.category.application.use_cases.create_category import CreateCategory, CreateCategoryRequest
from django_project.category_app.serializers import CreateCategoryResponseSerializer, CreateCategorySerializer, DeleteCategoryRequestSerializer, ListCategorySerializer, RetrieveCategoryRequestSerializer, RetrieveCategoryResponseSerializer, UpdateCategoryRequestSerializer
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest
from django_project.category_app.repository import DjangoORMCategoryRepository
from src.core.category.application.use_cases.list_category import ListCategory, ListCategoryRequest



class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:

        input = ListCategoryRequest()

        use_case = ListCategory(repository=DjangoORMCategoryRepository())
        output = use_case.execute(input)

        serializers = ListCategorySerializer(instance=output)


        return Response(status=status.HTTP_200_OK, data=serializers.data)
    
    def retrieve(self, request: Request, pk=None) -> Response:
        serializers = RetrieveCategoryRequestSerializer(data={"id": pk})
        serializers.is_valid(raise_exception=True)
        
        use_case = GetCategory(repository=DjangoORMCategoryRepository())


        category_pk = serializers.validated_data["id"]
        try:
            
            result = use_case.execute(request=GetCategoryRequest(id=category_pk))
        except CategoryNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": f"Category not found with id {category_pk}"})
        
        

        category_output = RetrieveCategoryResponseSerializer(instance=result).data

        return Response(status=status.HTTP_200_OK, data=category_output)
    

    def create(self, request: Request) -> Response:
        serializer = CreateCategorySerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        input = CreateCategoryRequest(**serializer.validated_data)

        use_case = CreateCategory(repository=DjangoORMCategoryRepository())

        output = use_case.execute(request=input)

        return Response(
            status=status.HTTP_201_CREATED, 
            data=CreateCategoryResponseSerializer(instance=output).data
        )
    
    def update(self, request: Request, pk=None) -> Response:
        serializer = UpdateCategoryRequestSerializer(data={"id": pk, **request.data})

        serializer.is_valid(raise_exception=True)

        input = UpdateCategoryRequest(**serializer.validated_data)

        use_case = UpdateCategory(repository=DjangoORMCategoryRepository())

        use_case.execute(request=input)

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request: Request, pk=None) -> Response:
        serializer = DeleteCategoryRequestSerializer(data={"id": pk})

        serializer.is_valid(raise_exception=True)

        use_case = DeleteCategory(repository=DjangoORMCategoryRepository())

        use_case.execute(request=DeleteCategoryRequest(**serializer.validated_data))
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def partial_update(self, request, pk: UUID = None) -> Response:
        serializer = UpdateCategoryRequestSerializer(data={
            **request.data,
            "id": pk,
        }, partial=True)
        serializer.is_valid(raise_exception=True)

        input = UpdateCategoryRequest(**serializer.validated_data)
        use_case = UpdateCategory(repository=DjangoORMCategoryRepository())
        try:
            use_case.execute(request=input)
        except CategoryNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response({"message": "Category updated successfully"}, status=status.HTTP_204_NO_CONTENT)

