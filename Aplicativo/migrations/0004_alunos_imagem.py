# Generated by Django 5.0.6 on 2024-08-20 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aplicativo', '0003_admins_acoes_alter_imgcarrossel_img1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='alunos',
            name='imagem',
            field=models.FileField(null=True, upload_to='imagem_alunos'),
        ),
    ]
