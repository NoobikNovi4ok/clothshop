from django.db import models


class Size(models.Model):
    SIZE_CHOICES = [
        ("S", "S"),
        ("M", "M"),
        ("L", "L"),
        ("XL", "XL"),
    ]
    size_label = models.CharField(max_length=10, choices=SIZE_CHOICES)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.size_label}"


class Color(models.Model):
    COLOR_CHOICES = [
        ("Red", "Красный"),
        ("Purple", "Фиолетовый"),
        ("Black", "Чёрный"),
        ("Grey", "Серый"),
        ("Blue", "Синий"),
    ]
    color_label = models.CharField(max_length=10, choices=COLOR_CHOICES)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.color_label}"


class Categories(models.Model):
    name = models.CharField(max_length=50, verbose_name="Имя категории")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL")
    icon = models.ImageField(upload_to="icon_category", verbose_name="Иконка")

    class Meta:
        verbose_name = "Категорию"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.name}"


class Countries(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название страны")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL")

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return f"{self.name}"


class Cloths(models.Model):
    name = models.CharField(max_length=55, verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL")
    photo = models.ImageField(upload_to="cloths_images", verbose_name="Фотография")
    description = models.CharField(
        max_length=2000, verbose_name="Описание", blank=True, null=True
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    cost = models.DecimalField(
        default=0.00, max_digits=7, decimal_places=2, verbose_name="Цена"
    )
    category = models.ForeignKey(
        to=Categories, on_delete=models.PROTECT, verbose_name="Категория"
    )
    country = models.ForeignKey(
        to=Countries, on_delete=models.PROTECT, verbose_name="Страна"
    )
    year = models.PositiveIntegerField(blank=True, null=True)
    sizes = models.ManyToManyField(Size, related_name="sizing_items")
    colors = models.ManyToManyField(Color, related_name="coloring_items")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ("pk",)

    def __str__(self):
        return f"{self.name}"
