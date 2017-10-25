# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 03:28
from __future__ import unicode_literals

from django.db import migrations


def alter_duplicates(apps, schema_editor):
    """
    Add a number beside duplicate items in existing databases.
    """
    List = apps.get_model("lists", "List")
    for list_ in List.objects.all():
        items = list_.item_set.all()
        texts = set()
        for ix, item in enumerate(items):
            if item.text in texts:
                item.text = f'{item.text} ({ix})'
                item.save()
            texts.add(item.text)


def remove_blank_items(apps, schema_editor):
    """
    Remove blank items in existing lists.
    """
    Item = apps.get_model("lists", "Item")
    for item in Item.objects.all():
        if item.text == '':
            item.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0004_item_list'),
    ]

    operations = [
        migrations.RunPython(alter_duplicates),
        migrations.RunPython(remove_blank_items),
    ]
