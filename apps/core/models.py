from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from timezone_field import TimeZoneField

from apps.core.utils import normalize_phone
from apps.core.validators import validate_phone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Метод создает пользователя с email в качестве логина и переданным паролем.
        """
        if not email or not password:
            raise ValueError("Адрес электронной почты и пароль должны быть заполнены")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("is_email_confirmed", False)
        extra_fields.setdefault("is_phone_confirmed", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Администратор должен иметь параметр is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя.
    """

    email = models.EmailField("Электронная почта", unique=True)
    is_email_confirmed = models.BooleanField(
        "Электронная почта подтверждена",
        default=False,
    )
    phone = models.CharField(
        "Сотовый телефон",
        max_length=16,
        unique=True,
        null=True,
        blank=True,
        validators=[validate_phone],
    )
    is_phone_confirmed = models.BooleanField(
        "Сотовый телефон подтвержден",
        default=False,
    )
    first_name = models.CharField("Имя", max_length=30)
    last_name = models.CharField("Фамилия", max_length=30)
    middle_name = models.CharField("Отчество", max_length=30, blank=True)
    timezone = TimeZoneField("Часовой пояс", default="Europe/Moscow")
    agreement = models.BooleanField("Согласие на обработку данных", default=False)
    joined = models.DateTimeField("Дата и время регистрации", auto_now_add=True)
    updated = models.DateTimeField("Дата и время обновления", auto_now=True)
    is_active = models.BooleanField("Активный", default=False)
    is_staff = models.BooleanField("Доступ в админ. панель", default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-updated", "-joined", "last_name", "first_name", "middle_name"]

    def get_full_name(self):
        """
        Возвращает полное имя (фамилия, имя и отчество, разделенные пробелом).
        """
        return (
            f"{self.last_name} {self.first_name}" + f" {self.middle_name}"
            if self.middle_name
            else ""
        )

    def get_short_name(self):
        """
        Возвращает краткое имя (фамилия + инициалы).
        """
        return (
            f"{self.last_name} {self.first_name[0]}." + f" {self.middle_name[0]}."
            if self.middle_name
            else ""
        )

    get_short_name.short_description = "Краткое имя"

    def update(self, **kwargs):
        """
        Метод обновляет объект пользователя.
        """
        for field, value in kwargs.items():
            if hasattr(self, field):
                if field == "phone":
                    value = normalize_phone(value)
                setattr(self, field, value)
        self.save()


class UserProfile(models.Model):
    class Sex(models.TextChoices):
        MALE = "MALE", "мужской"
        FEMALE = "FEMALE", "женский"
        UNDEFINED = "UNDEFINED", "не определено"

    user = models.OneToOneField(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )
    sex = models.CharField(
        "Пол",
        max_length=9,
        default=Sex.UNDEFINED,
        choices=Sex.choices,
    )
    birthday = models.DateField("День рождения", blank=True, null=True)
    # BIRTH_YEAR_CHOICES = [year for year in range(1950, datetime.date.today().year + 1, 1)]
    age = models.IntegerField(
        "Возраст",
        validators=[
            MinValueValidator(0, "Возраст не может быть меньше 0 лет"),
            MaxValueValidator(100, "Возраст не может быть больше 100 лет"),
        ],
        blank=True,
        null=True,
    )
    height = models.IntegerField(
        "Рост",
        help_text="Введите Ваш рост в см.",
        validators=[
            MinValueValidator(40, "Рост не может быть меньше 40 см"),
            MaxValueValidator(300, "Рост не может быть больше 300 см"),
        ],
        blank=True,
        null=True,
    )
    weight = models.IntegerField(
        "Вес",
        help_text="Введите Ваш вес в кг.",
        validators=[
            MinValueValidator(1, "Вес не может быть меньше 1 кг"),
            MaxValueValidator(300, "Вес не может быть больше 300 кг"),
        ],
        blank=True,
        null=True,
    )
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def update(self, **kwargs):
        """
        Метод обновляет объект профиля пользователя.
        """
        for field, value in kwargs.items():
            if hasattr(self, field):
                setattr(self, field, value)
        self.save()
