from rest_framework.response import Response

from .serializers import *
from rest_framework import viewsets, status


class UsersViewsets(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializers


class CoordsViewsets(viewsets.ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializers


class LevelViewsets(viewsets.ModelViewSet):
    queryset = Levl.objects.all()
    serializer_class = LevlSerializers


class ImagesViewsets(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializers


class PerevalViewsets(viewsets.ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializers
    filterset_fields = ('user__email',)

    def create(self, request, *args, **kwargs):
        serializer = PerevalSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_200_OK,
                'messag': None,
                'id': serializer.data['id'],
            })
        if status.HTTP_400_BAD_REQUEST:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'messag': 'Bad request',
                'id': None,
            })
        if status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'messag': 'Ошибка подключения к базе',
                'id': None,
            })

    def partial_update(self, request, *args, **kwargs):
        pereval = self.get_object()
        if pereval.status == 'new':
            serializer = PerevalSerializers(pereval, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'state': '1',
                    'message': 'Запись обновлена',
                })
            else:
                return Response({
                    'state': '0',
                    'message': serializer.errors
                })
        else:
            return Response({
                'state': '0',
                'message': f'Отклонено: {pereval.get_status_display()}'
            })