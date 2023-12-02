from django.db import models


class User(models.Model):
   email = models.EmailField(max_length=64, unique=False)
   phone = models.CharField(max_length=12, verbose_name='Телефон')
   fam = models.CharField(max_length=64, verbose_name='Фамилия')
   name = models.CharField(max_length=64, verbose_name='Имя')
   otc = models.CharField(max_length=64, verbose_name='Отчество')

   def __str__(self):
      return f'{self.fam} {self.name} {self.email}'

   class Meta:
      verbose_name = "Турист"


class Coords(models.Model):
   latitude = models.FloatField(verbose_name='Широта')
   longitude = models.FloatField(verbose_name='Долгота')
   height = models.IntegerField(verbose_name='Высота')

   def __str__(self):
      return f"широта: {self.latitude}, долгота: {self.longitude}, высота: {self.height}"

   class Meta:
        verbose_name = "Координаты"


class Level(models.Model):
   winter = models.CharField(max_length=64, verbose_name='Зима', null=True, blank=True)
   summer = models.CharField(max_length=64, verbose_name='Лето', null=True, blank=True)
   autumn = models.CharField(max_length=64, verbose_name='Осень', null=True, blank=True)
   spring = models.CharField(max_length=64, verbose_name='Весна', null=True, blank=True)

   def __str__(self):
      return f"зима: {self.winter}, весна: {self.spring}, лето: {self.summer}, осень: {self.autumn}"

   class Meta:
      verbose_name = "Уровень сложности"


class Pereval(models.Model):
   SELECT = (
      ("new", "новый"),
      ("pending", "в работе"),
      ("accepted", "принят"),
      ("rejected", "отклонён"),
   )
   add_time = models.DateTimeField()
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   coords = models.ForeignKey(Coords, on_delete=models.CASCADE)
   level = models.ForeignKey(Level, on_delete=models.CASCADE)
   beauty_title = models.TextField(blank=True, verbose_name='Основное название вершины', null=True)
   title = models.CharField(max_length=64, blank=True, null=True, verbose_name='Название вершины')
   other_titles = models.CharField(max_length=64, blank=True, null=True, verbose_name='Другое название')
   connect = models.CharField(max_length=64, blank=True, verbose_name='Связывает', null=True)
   status = models.CharField(max_length=64, choices=SELECT, default=SELECT[0][0])

   def __str__(self):
      return f'{self.pk} {self.add_time} {self.beauty_title}'


class Images(models.Model):
   pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE, related_name='images')
   data = models.URLField(verbose_name='Изображение', null=True, blank=True)
   # data = models.ImageField(upload_to='images/', verbose_name='Изображение')
   title = models.TextField(max_length=64, null=True, blank=True)

   def __str__(self):
      return f"{self.pk} {self.data}"
