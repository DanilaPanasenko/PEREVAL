from .models import *
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer


class UsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('email', 'last_name', 'first_name', 'patronymic', 'phone')


class CoordsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ('latitude', 'longitude', 'height')


class LevlSerializers(serializers.ModelSerializer):
    class Meta:
        model = Levl
        fields = ('level_winter', 'level_spring', 'level_summer', 'level_autumn')


class ImagesSerializers(serializers.ModelSerializer):
    image = serializers.URLField()


    class Meta:
        model = Images
        fields = ('image', 'title')


class PerevalSerializers(WritableNestedModelSerializer):
    add_time = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)
    user = UsersSerializers()
    coords = CoordsSerializers()
    level = LevlSerializers(allow_null=True)
    images = ImagesSerializers(many=True)
    status = serializers.CharField()


    class Meta:
        model = Pereval
        depth = 1
        fields = (
            'id',
            'beauty_title',
            'title',
            'other_titles',
            'add_time',
            'user',
            'coords',
            'level',
            'status',
            'connect',
            'images',
        )

        def create(self, validated_data, **kwargs):
            user = validated_data.pop('user')
            coords = validated_data.pop('coords')
            level = validated_data.pop('level')
            images = validated_data.pop('images')

            user, created = Users.objects.get_or_create(**user)

            coords = Coords.objects.create(**coords)
            level = Levl.objects.create(**level)
            perev = Pereval.objects.create(**validated_data, user=user, coords=coords, level=level, status='new')

            for image in images:
                data = image.pop('data')
                title = image.pop('title')
                Images.objects.create(data=data, perev=perev, title=title)
            return perev

        def validate(self, data):
            if self.instance is not None:
                instance_user = self.instance.user
                data_user = data.get('user')
                validating_user_fields = [
                    instance_user.email != data_user['email'],
                    instance_user.last_name != data_user['last_name'],
                    instance_user.first_name != data_user['first_name'],
                    instance_user.patronymic != data_user['patronymic'],
                    instance_user.phone != data_user['phone'],
                ]
                if data_user is not None and any(validating_user_fields):
                    raise serializers.ValidationError({'Отклонено': 'нельзя изменять данные пользователя'})
            return data
