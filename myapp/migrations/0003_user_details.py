# Generated by Django 3.0.4 on 2020-03-13 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_category_master_company_details_data_set_product_master_product_pic_product_review_sub_category_mast'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_name', models.CharField(max_length=150)),
                ('l_name', models.CharField(max_length=150)),
                ('dob', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=15)),
                ('addr', models.CharField(max_length=1500)),
                ('pincode', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=250)),
                ('contact', models.CharField(max_length=50)),
                ('dt', models.CharField(max_length=50)),
                ('tm', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
            ],
        ),
    ]