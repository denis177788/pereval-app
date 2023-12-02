from .models import *
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):

    def save(self, **kwargs):
        self.is_valid()
        user = User.objects.filter(email=self.validated_data.get('email'))
        if user.exists():
            return user.first()
        else:
            new_user = User.objects.create(
                email=self.validated_data.get('email'),
                phone=self.validated_data.get('phone'),
                fam=self.validated_data.get('fam'),
                name=self.validated_data.get('name'),
                otc=self.validated_data.get('otc'),
            )
            new_user.save()
            return new_user

    class Meta:
        model = User
        fields = ['fam', 'name', 'otc', 'email', 'phone']
        verbose_name = 'Турист'


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
        read_only_fields = ['pereval']


# основной сериалайзер с вложенными данными
class PerevalSerializer(WritableNestedModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer(allow_null=True)
    images = ImagesSerializer(many=True, allow_null=True)

    class Meta:
        model = Pereval
        fields = (
            'id', 'status', 'add_time', 'beauty_title', 'title', 'other_titles', 'connect', 'user', 'coords', 'images', 'level')
        read_only_fields = ['id', 'status']

    # выполняет ТЗ о невозможности изменять данные пользователя при редактировании данных о перевале
    def validate(self, data):
        if self.instance is not None:
            instance_user = self.instance.user
            data_user = data.get('user')
            validating_user_fields = [
                instance_user.fam != data_user['fam'],
                instance_user.name != data_user['name'],
                instance_user.otc != data_user['otc'],
                instance_user.phone != data_user['phone'],
                instance_user.email != data_user['email'],
            ]
            if data_user is not None and any(validating_user_fields):
                raise serializers.ValidationError({'Данные пользователя не могут быть изменены'})
        return data

    # Сохранение данных о перевале, полученных от пользователя
    # def create(self, validated_data, **kwargs):
    #     user = validated_data.pop('user')
    #     coords = validated_data.pop('coords')
    #     level = validated_data.pop('level')
    #     images = validated_data.pop('images')
    #
    #     pick_user = User.objects.filter(email=user['email'])
    #     if pick_user.exists():
    #         user = pick_user.first()
    #     else:
    #         user = User.objects.create(**user)
    #
    #     coords = Coords.objects.create(**coords)
    #     level = Level.objects.create(**level)
    #     pereval = Pereval.objects.create(**validated_data, user=user, coords=coords, level=level, status='new')
    #
    #     for image in images:
    #         data = image.pop('data')
    #         title = image.pop('title')
    #         Images.objects.create(data=data, pereval=pereval, title=title)
    #
    #     return pereval
