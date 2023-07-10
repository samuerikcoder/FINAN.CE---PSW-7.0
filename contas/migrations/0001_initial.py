# Generated by Django 4.2.3 on 2023-07-08 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('perfil', '0002_conta'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContaPagar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('descricao', models.TextField()),
                ('dia_pagamento', models.IntegerField()),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='perfil.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='ContaPaga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_pagamento', models.DateField()),
                ('conta', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='contas.contapagar')),
            ],
        ),
    ]
