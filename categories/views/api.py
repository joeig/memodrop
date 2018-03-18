from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from categories.serializers import CategorySerializer
from categories.views.gui import CategoryBelongsUserMixin


class APICategoryList(CategoryBelongsUserMixin, generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer


class APICategoryDetail(CategoryBelongsUserMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
