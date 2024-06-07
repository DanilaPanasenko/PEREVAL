from django.db import models


class Users(models.Model):
    email = models.EmailField(max_length=40, verbose_name='Email')
    last_name = models.CharField(max_length=40, verbose_name='Фамилия')
    first_name = models.CharField(max_length=40, verbose_name='Имя')
    patronymic = models.CharField(max_length=40, verbose_name='Отчество')
    phone = models.CharField(max_length=40, verbose_name='Номер телефона')


    # class Meta:
    #     verbose_name = 'Турист'
    #     verbose_name_many = 'Туристы'

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}"


class Coords(models.Model):
    latitude = models.FloatField(max_length=20, verbose_name='Широта', blank=True, null=True)
    longitude = models.FloatField(max_length=20, verbose_name='Долгота', blank=True, null=True)
    height = models.IntegerField(verbose_name='Высота', blank=True, null=True)

    def __str__(self):
        return f'широта:{self.latitude}, долгота:{self.longitude}, высота:{self.height}'

    # class Meta:
    #     verbose_name = 'Координаты'
    #     verbose_name_many = 'Координаты'


class Levl(models.Model):
    winter = '4A'
    spring = '2A'
    summer = '1A'
    autumn = '3A'

    LEVEL_CHOICES = [
        ('4A', winter),
        ('2A', spring),
        ('1A', summer),
        ('3A', autumn),
    ]

    level_winter = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=winter)
    level_spring = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=winter)
    level_summer = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=winter)
    level_autumn = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=winter)

    def __str__(self):
        return f'зима:{self.level_winter}, весна:{self.level_spring,}, лето:{self.level_summer,}, осень:{self.level_autumn,}'


    # class Meta:
    #     verbose_name = 'Уровень сложности'
    #     verbose_name_many = 'Уровень сложности'


class Pereval(models.Model):
    new = 'new'
    pending = 'pending'
    accepted = 'accepted'
    rejected = 'rejected'
    STATUS = [
        (new, 'новый'),
        (pending, 'модератор взял в работу'),
        (accepted, 'модерация прошла успешно'),
        (rejected, 'информация не принята')
    ]

    beauty_title = models.CharField(max_length=255, verbose_name='Названия припятствия', blank=True, null=True)
    title = models.CharField(max_length=255, verbose_name='Вершина', blank=True, null=True)
    other_titles = models.CharField(max_length=255, verbose_name='Другое название', blank=True, null=True)
    add_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='user')
    coords = models.ForeignKey(Coords, on_delete=models.CASCADE, blank=True, null=True)
    level = models.ForeignKey(Levl, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default=new)
    connect = models.TextField(blank=True, null=True)


class Images(models.Model):
    image = models.ImageField(upload_to='static/images')
    title = models.CharField(max_length=125)
    pereval_id = models.ForeignKey(Pereval, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.title
