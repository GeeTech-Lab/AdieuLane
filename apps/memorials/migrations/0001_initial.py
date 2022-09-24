# Generated by Django 3.2.15 on 2022-09-23 20:05

import adieulane.validators
import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BurialMemory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Mr, Mrs, Miss, Sir....', max_length=100)),
                ('first_name', models.CharField(help_text='John', max_length=100)),
                ('last_name', models.CharField(help_text='Ezeh', max_length=100)),
                ('other_names', models.CharField(blank=True, help_text='Other titled names...', max_length=100, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], default='Others', help_text='Male/Female', max_length=100, null=True)),
                ('slug', models.SlugField(unique=True)),
                ('image', cloudinary.models.CloudinaryField(blank=True, help_text='The deceased image', max_length=255, null=True)),
                ('date_of_birth', models.DateField()),
                ('date_of_death', models.DateField()),
                ('place_of_birth', models.CharField(blank=True, help_text='City, State, Country', max_length=220, null=True)),
                ('place_of_death', models.CharField(blank=True, help_text='City, State, Country', max_length=220, null=True)),
                ('cause_of_death', models.CharField(blank=True, help_text='Sickness, Accident...', max_length=200, null=True)),
                ('brief_biography', models.TextField(blank=True, help_text='Brief biography...', null=True)),
                ('education', models.TextField(blank=True, help_text='Education...', null=True)),
                ('work_life', models.TextField(blank=True, help_text='Work life...', null=True)),
                ('family_biography', models.TextField(blank=True, help_text="Family's origin/history...", null=True)),
                ('burial_ceremony_address', models.CharField(blank=True, help_text='Street, Town, City, State, Country', max_length=220, null=True)),
                ('accept_donations', models.BooleanField(default=False, help_text='Accept burial levy donation for the deceased?...')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memories', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'BurialMemories',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='MemoryTribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tribute_text', models.TextField()),
                ('category', models.CharField(choices=[('candle', 'candle'), ('flower', 'flower'), ('note', 'note')], default='candle', max_length=200)),
                ('on', models.DateTimeField(auto_now=True)),
                ('burial_memory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memory_tributes', to='memorials.burialmemory')),
                ('by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tributes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MemoryGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, help_text='What was the event and where was it taken?...', null=True)),
                ('image', cloudinary.models.CloudinaryField(blank=True, help_text='The deceased memory image', max_length=255, null=True, validators=[adieulane.validators.MaxSizeValidator(5)])),
                ('video', models.URLField(blank=True, help_text='video youtube link', null=True)),
                ('audio', cloudinary.models.CloudinaryField(blank=True, help_text='The deceased memory audio', max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('burial_memory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='galleries', to='memorials.burialmemory')),
                ('by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='galleries', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'MemoryGalleries',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='FamilyTree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Mr, Mrs, Miss, Sir....', max_length=100)),
                ('guest_full_name', models.CharField(help_text='full name(John Ezeh)...', max_length=100)),
                ('image', cloudinary.models.CloudinaryField(blank=True, help_text='The deceased memory image', max_length=255, null=True)),
                ('relationship', models.CharField(choices=[('father', 'father'), ('mother', 'mother'), ('son', 'son'), ('daughter', 'daughter'), ('husband', 'husband'), ('wife', 'wife'), ('brother', 'brother'), ('sister', 'sister'), ('grandfather', 'grandfather'), ('grandmother', 'grandmother'), ('grandson', 'grandson'), ('granddaughter', 'granddaughter'), ('uncle', 'uncle'), ('aunt', 'aunt'), ('nephew', 'nephew'), ('niece', 'niece'), ('cousin', 'cousin'), ('friend', 'friend'), ('friend with family', 'friend with family')], help_text='Relationship with the deceased...', max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('burial_memory', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='family_trees', to='memorials.burialmemory')),
                ('user_full_name', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='family_trees', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'FamilyTrees',
                'ordering': ('-created',),
            },
        ),
    ]
