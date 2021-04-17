# Generated by Django 3.1.8 on 2021-04-17 15:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vehicle', '0002_auto_20210417_2201'),
    ]

    operations = [
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=32)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner_updated_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='person_id',
        ),
        migrations.DeleteModel(
            name='Person',
        ),
        migrations.AddField(
            model_name='vehicle',
            name='owner_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vehicle.owner'),
        ),
    ]
