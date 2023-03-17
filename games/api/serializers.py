from rest_framework import serializers
from games.models import Developer, Game
from datetime import datetime
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')

class DeveloperSerializer(serializers.ModelSerializer):

    class Meta:
        model = Developer
        fields = '__all__'

    def validate_age(self, data_value):
        if data_value < 21:
            raise serializers.ValidationError(f'Developer yaşı 21 den küçük olamaz')
        return data_value

class GameSerializer(serializers.ModelSerializer):

    # creator = UserSerializer(read_only=True)
    # developer = DeveloperSerializer(read_only=True)

    class Meta:
        model = Game
        fields = '__all__'
        read_only_fields = ['id']

    def validate_publication_date(self, date_value):
        now = datetime.now()
        if date_value > now:
            raise serializers.ValidationError('Yayımlanma tarihi ileri bir tarih olamaz!')
        return date_value


class GameSearchSerializer(serializers.ModelSerializer):

    creator = UserSerializer()
    developer = DeveloperSerializer()

    class Meta:
        model = Game
        fields = '__all__'
        read_only_fields = ['id']
