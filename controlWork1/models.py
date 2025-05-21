from django.db import models
from django.core.validators import MinValueValidator


class Exhibition(models.Model):
    title = models.CharField("Название выставки", max_length=255, unique=True)
    info = models.TextField("Краткая информация")
    all_info = models.TextField("Полная информация")
    img = models.ImageField(
        "Изображение", upload_to="exhibitions_images/", null=True, blank=True
    )
    price = models.IntegerField(
        "Цена (руб.)",
        validators=[MinValueValidator(0, "Цена не может быть отрицательной.")],
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Выставка"
        verbose_name_plural = "Выставки"
        ordering = ["id"]


class Show(models.Model):
    title = models.CharField("Название шоу", max_length=255, unique=True)
    info = models.TextField("Краткая информация")
    all_info = models.TextField("Полная информация")
    img = models.ImageField(
        "Изображение", upload_to="shows_images/", null=True, blank=True
    )
    price = models.IntegerField(
        "Цена (руб.)",
        validators=[MinValueValidator(0, "Цена не может быть отрицательной.")],
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Шоу"
        verbose_name_plural = "Шоу"
        ordering = ["id"]

class Sale(models.Model):
    title = models.CharField("Категория", max_length=100, unique=True)
    discount_percent_value = models.IntegerField("Процент скидки (число)", null=True, blank=True)
    required_document = models.CharField("Требуемый документ", max_length=255)

    def __str__(self):
        return f"{self.title} ({self.discount_percent_value})"

    class Meta:
        verbose_name = "Скидка/Акция"
        verbose_name_plural = "Скидки и Акции"
        ordering = ['id']

class Student(models.Model):
    name = models.CharField("ФИО студента", max_length=255, unique=True) 
    image_url = models.URLField("URL изображения", max_length=500, blank=True, null=True)
    email = models.EmailField("Email", blank=True, null=True)
    number = models.CharField("Номер телефона", max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        ordering = ['name']

class Program(models.Model):
    title = models.CharField("Название программы", max_length=255, unique=True)
    description = models.TextField("Описание программы")
    
    head_name = models.CharField("ФИО руководителя", max_length=255, blank=True, null=True)
    head_image_url = models.URLField("URL фото руководителя", max_length=500, blank=True, null=True)
    head_email = models.EmailField("Email руководителя", blank=True, null=True)
    
    manager_name = models.CharField("ФИО менеджера", max_length=255, blank=True, null=True) 
    manager_image_url = models.URLField("URL фото менеджера", max_length=500, blank=True, null=True)
    manager_email = models.EmailField("Email менеджера", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Образовательная программа"
        verbose_name_plural = "Образовательные программы"
        ordering = ['title']

class Painter(models.Model):
    name = models.CharField("Имя художника", max_length=255, unique=True)
    info = models.TextField("Общая информация о художнике")
    
    numbered_list_title = models.CharField("Заголовок нумерованного списка", max_length=255, blank=True, null=True)
    numbered_list_content_json = models.JSONField("Содержимое нумерованного списка (JSON)", blank=True, null=True, default=list) 

    bulleted_list_title = models.CharField("Заголовок маркированного списка", max_length=255, blank=True, null=True)
    bulleted_list_content_json = models.JSONField("Содержимое маркированного списка (JSON)", blank=True, null=True, default=list)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Художник"
        verbose_name_plural = "Художники"
        ordering = ['name']
    
class PainterImage(models.Model):
    painter = models.ForeignKey(Painter, related_name='images', on_delete=models.CASCADE, verbose_name="Художник")
    picture_url = models.URLField("URL изображения", max_length=500)
    caption = models.CharField("Подпись к изображению", max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Изображение для {self.painter.name} - {self.caption or 'Без подписи'}"

    class Meta:
        verbose_name = "Изображение художника"
        verbose_name_plural = "Изображения художников"
        ordering = ['painter', 'id']

class ArtistCategory(models.Model):
    name = models.CharField("Название категории", max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория художника"
        verbose_name_plural = "Категории художников"
        ordering = ['name']

class Artist(models.Model):
    category = models.ForeignKey(ArtistCategory, related_name='artists_in_category', on_delete=models.CASCADE, verbose_name="Категория")
    name = models.CharField("Имя художника", max_length=255, unique=True) 
    years = models.CharField("Годы жизни", max_length=50, blank=True, null=True)
    style = models.CharField("Стиль/направление", max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Известный художник"
        verbose_name_plural = "Известные художники"
        ordering = ['category', 'name']

class ArtistWork(models.Model):
    artist = models.ForeignKey(Artist, related_name='works_of_artist', on_delete=models.CASCADE, verbose_name="Художник")
    title = models.CharField("Название работы", max_length=255)

    def __str__(self):
        return f"{self.title} ({self.artist.name})"

    class Meta:
        verbose_name = "Работа художника"
        verbose_name_plural = "Работы художников"
        ordering = ['artist', 'title']

class GalleryPainting(models.Model):
    title = models.CharField("Название картины", max_length=255)
    info = models.TextField("Описание картины")
    image_url = models.URLField("URL изображения", max_length=500)
    painter_name = models.CharField("Имя художника", max_length=255)

    def __str__(self):
        return f"{self.title} - {self.painter_name}"

    class Meta:
        verbose_name = "Картина в галерее"
        verbose_name_plural = "Картины в галерее"
        ordering = ['title']

class Order(models.Model):
    name = models.CharField("Имя", max_length=100)
    surname = models.CharField("Фамилия", max_length=100)
    patronymic = models.CharField("Отчество", max_length=100, blank=True, default="")
    birth_date = models.DateField("Дата Рождения")
    phone_number = models.CharField("Номер телефона", max_length=20)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return f"Заказ {self.id} от {self.surname} {self.name}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]


class CanvasType(models.Model):
    name = models.CharField("Название типа холста", max_length=100, unique=True)
    price_per_sq_cm = models.DecimalField(
        "Цена за см² (руб.)",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01, "Цена должна быть положительной.")],
    )

    def __str__(self):
        return f"{self.name} ({self.price_per_sq_cm} руб/см²)"

    class Meta:
        verbose_name = "Тип холста"
        verbose_name_plural = "Типы холстов"
        ordering = ["price_per_sq_cm", "name"]


class MaterialType(models.Model):
    name = models.CharField("Название типа материалов", max_length=100, unique=True)
    price_per_sq_cm = models.DecimalField(
        "Цена за см² (руб.)",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01, "Цена должна быть положительной.")],
    )

    def __str__(self):
        return f"{self.name} ({self.price_per_sq_cm} руб/см²)"

    class Meta:
        verbose_name = "Тип материалов"
        verbose_name_plural = "Типы материалов"
        ordering = ["price_per_sq_cm", "name"]


class ArtworkCostCalculation(models.Model):
    height = models.IntegerField(
        "Высота картины (см)",
        validators=[MinValueValidator(1, "Высота должна быть не менее 1 см.")],
    )
    width = models.IntegerField(
        "Ширина картины (см)",
        validators=[MinValueValidator(1, "Ширина должна быть не менее 1 см.")],
    )
    canvas_type = models.ForeignKey(
        CanvasType, on_delete=models.PROTECT, verbose_name="Тип холста"
    )
    material_type = models.ForeignKey(
        MaterialType, on_delete=models.PROTECT, verbose_name="Тип материалов"
    )
    result_cost = models.IntegerField(
        "Итоговая стоимость (руб.)", null=True, blank=True
    )
    calculated_at = models.DateTimeField("Время расчета", auto_now_add=True)

    def __str__(self):
        cost_display = (
            f"{self.result_cost} руб."
            if self.result_cost is not None
            else "еще не рассчитано"
        )
        return f"Расчет от {self.calculated_at.strftime('%d.%m.%Y %H:%M')} - {cost_display}"

    class Meta:
        verbose_name = "Расчет стоимости картины"
        verbose_name_plural = "Расчеты стоимости картин"
        ordering = ["-calculated_at"]
