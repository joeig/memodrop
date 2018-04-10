from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from cards.serializers import CardSerializer
from cards.views.gui import CardBelongsOwnerMixin


class APICardList(CardBelongsOwnerMixin, generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CardSerializer


class APICardDetail(CardBelongsOwnerMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CardSerializer
