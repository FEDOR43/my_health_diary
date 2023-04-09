# Generated by Django 4.2 on 2023-04-09 14:23

import apps.core.models
import apps.core.validators
from django.db import migrations, models
import timezone_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Электронная почта')),
                ('is_email_confirmed', models.BooleanField(default=False, verbose_name='Электронная почта подтверждена')),
                ('phone', models.CharField(blank=True, max_length=16, null=True, unique=True, validators=[apps.core.validators.PhoneValidator()], verbose_name='Сотовый телефон')),
                ('is_phone_confirmed', models.BooleanField(default=False, verbose_name='Сотовый телефон подтвержден')),
                ('first_name', models.CharField(max_length=30, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=30, verbose_name='Фамилия')),
                ('middle_name', models.CharField(blank=True, max_length=30, verbose_name='Отчество')),
                ('sex', models.CharField(choices=[('MALE', 'мужской'), ('FEMALE', 'женский'), ('UNDEFINED', 'не определено')], default='UNDEFINED', max_length=9, verbose_name='Пол')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='День рождения')),
                ('age', models.DateField(blank=True, null=True, verbose_name='Возраст')),
                ('timezone', timezone_field.fields.TimeZoneField(default='Europe/Moscow', verbose_name='Часовой пояс')),
                ('agreement', models.BooleanField(default=False, verbose_name='Согласие на обработку данных')),
                ('joined', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время регистрации')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата и время обновления')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активный')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Доступ в админ. панель')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ['-updated', '-joined', 'last_name', 'first_name', 'middle_name'],
            },
            managers=[
                ('objects', apps.core.models.UserManager()),
            ],
        ),
    ]
