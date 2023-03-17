from rest_framework.views import APIView
from games.models import Developer, Game
from games.api.serializers import GameSerializer, DeveloperSerializer,GameSearchSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from games.api.filters import DeveloperFilter, GameFilter
from rest_framework.pagination import LimitOffsetPagination
import abc
from django.http import HttpResponse
from games.documents import DeveloperDocument, GameDocument
from elasticsearch_dsl import Q


class DeveloperListCreateAPIView(ListCreateAPIView):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = DeveloperFilter


class DeveloperRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer
    permission_classes = [IsAuthenticated]


class GameListCreateAPIView(ListCreateAPIView):
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = GameFilter

    def get_user(self):
        if self.request.user.is_authenticated:
            return self.request.user
        else:
            return None

    def get_queryset(self):
        user = self.get_user()
        queryset = Game.objects.all()
        if user:
            queryset = queryset.filter(creator=user)
        return queryset

    # def perform_create(self, serializer):
    #     serializer.save(creator=None)


class GameRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]


class PaginatedElasticSearchAPIView(APIView, LimitOffsetPagination):
    serializer_class = None
    document_class = None

    @abc.abstractmethod
    def generate_q_expression(self, query):
        """This method should be overridden
        and return a Q() expression."""

    def get(self, request, query):
        try:
            q = self.generate_q_expression(query)
            search = self.document_class.search().query(q)
            response = search.execute()

            print(f'Found {response.hits.total.value} hit(s) for query: "{query}"')

            results = self.paginate_queryset(response, request, view=self)

            print(results)
            serializer = self.serializer_class(results, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            return HttpResponse(e, status=500)


class SearchDevelopers(PaginatedElasticSearchAPIView):
    serializer_class = DeveloperSerializer
    document_class = DeveloperDocument

    def generate_q_expression(self, query):
        return Q('bool',
                 should=[
                     Q('match', username=query),
                     Q('match', full_name=query)
                 ], minimum_should_match=1)


class SearchGames(PaginatedElasticSearchAPIView):
    serializer_class = GameSearchSerializer
    document_class = GameDocument

    def generate_q_expression(self, query):
        return Q('multi_match', query=query,
                 fields=[
                     'name',
                     'description'
                 ], fuzziness='auto')
