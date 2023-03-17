from django.contrib.auth.models import User
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from games.models import Developer, Game

@registry.register_document
class DeveloperDocument(Document):
    class Index:
        name = 'developers'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Developer
        fields = [
            'id',
            'username',
            'full_name',
            'age',
        ]


@registry.register_document
class GameDocument(Document):
    creator = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'first_name': fields.TextField(),
        'last_name': fields.TextField(),
        'username': fields.TextField()
    })
    developer = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'username': fields.TextField(),
        'full_name': fields.TextField(),
        'age': fields.IntegerField()
    })
    class Index:
        name = 'games'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Game
        fields = [
            'name',
            'description',
            'publication_date',
            'status'
        ]
        read_only_fields = ['id']


