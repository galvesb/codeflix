from uuid import UUID
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from django_project.category_app.serializers import ListCategorySerializer, RetrieveCategoryRequestSerializer, RetrieveCategoryResponseSerializer
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


        return Response(status=HTTP_200_OK, data=serializers.data)
    
    def retrieve(self, request: Request, pk=None) -> Response:
        serializers = RetrieveCategoryRequestSerializer(data={"id": pk})
        serializers.is_valid(raise_exception=True)
        
        use_case = GetCategory(repository=DjangoORMCategoryRepository())


        category_pk = serializers.validated_data["id"]
        try:
            
            result = use_case.execute(request=GetCategoryRequest(id=category_pk))
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND, data={"detail": f"Category not found with id {category_pk}"})
        
        

        category_output = RetrieveCategoryResponseSerializer(instance=result).data

        return Response(status=HTTP_200_OK, data=category_output)
