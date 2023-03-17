import django_filters
from games.models import Game, Developer


class GameFilter(django_filters.FilterSet):
    class Meta:
        model = Game
        fields = {
            'creator__id': ['exact'],
            'developer__id': ['exact'],
            'name': ['icontains'],
            'description': ['icontains'],
            'publication_date': ['gte', 'lte'],
            'status': ['exact']
        }


class DeveloperFilter(django_filters.FilterSet):
    class Meta:
        model = Developer
        fields = {
            'username': ['icontains', 'exact'],
            'full_name': ['icontains', 'exact'],
            'age': ['gte', 'lte', 'exact']
        }
