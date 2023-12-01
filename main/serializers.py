from .models import *
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = User
       fields = ['fam', 'name', 'otc', 'email', 'phone']


class CoordsSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Coords
       fields = ['latitude', 'longitude', 'height', ]


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['winter', 'summer', 'autumn', 'spring', ]


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['pereval', 'data', 'title', ]


# основной сериалайзер с вложенными данными
class PerevalSerializer(WritableNestedModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer(allow_null=True)
    images = ImagesSerializer(many=True)

    class Meta:
        model = Pereval
        fields = (
            'add_time', 'beauty_title', 'title', 'other_titles', 'connect', 'user', 'coords', 'images', 'level')
        read_only_fields = ['status']

    # Сохранение данных о перевале, полученных от пользователя
    def create(self, validated_data, **kwargs):
        user = validated_data.pop('user')
        coords = validated_data.pop('coords')
        level = validated_data.pop('level')
        images = validated_data.pop('images')

        # проверка уникальности пользователя
        pick_user = User.objects.filter(email=user['email'])
        if pick_user.exists():
            user_serializer = UserSerializer(data=user)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
        else:
            user = User.objects.create(**user)

        coords = Coords.objects.create(**coords)
        level = Level.objects.create(**level)
        pereval = Pereval.objects.create(**validated_data, user=user, coords=coords, level=level, status='new')

        for image in images:
            data = image.pop('data')
            title = image.pop('title')
            Images.objects.create(data=data, pereval=pereval, title=title)

        return pereval

