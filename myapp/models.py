from django.db import models

# Create your models here.
class user_login(models.Model):
    uname = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    utype = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.id},{self.uname}'

class company_details(models.Model):
    c_name = models.CharField(max_length=150)
    c_descp = models.CharField(max_length=500)
    c_addr1 = models.CharField(max_length=350)
    c_addr2 = models.CharField(max_length=350)
    c_addr3 = models.CharField(max_length=350)
    c_pincode = models.CharField(max_length=50)
    c_email = models.CharField(max_length=250)
    c_contact1 = models.CharField(max_length=50)
    c_contact2 = models.CharField(max_length=50)
    c_url = models.CharField(max_length=250)
    c_dt = models.CharField(max_length=50)
    c_tm = models.CharField(max_length=50)
    c_status = models.CharField(max_length=50)
    c_logo = models.CharField(max_length=350)

    def __str__(self):
        return self.c_name

class user_details(models.Model):
    user_id = models.IntegerField()
    f_name = models.CharField(max_length=150)
    l_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=15)
    place = models.CharField(max_length=150)
    pincode = models.CharField(max_length=50)
    email = models.CharField(max_length=250)
    contact = models.CharField(max_length=50)
    dt = models.CharField(max_length=50)
    tm = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.user_id},{self.email}'

class category_master(models.Model):
    category_name = models.CharField(max_length=350)

    def __str__(self):
        return self.category_name

class sub_category_master(models.Model):
    sub_category_name = models.CharField(max_length=350)
    category_master_id = models.IntegerField()

    def __str__(self):
        return self.sub_category_name

class product_master(models.Model):
    product_name = models.CharField(max_length=150)
    company_details_id = models.IntegerField()
    sub_category_master_id = models.IntegerField()
    product_descp = models.CharField(max_length=500)
    product_price = models.FloatField()
    dt = models.CharField(max_length=50)
    tm = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.product_name

class product_review(models.Model):
    product_master_id = models.IntegerField()
    user_id = models.IntegerField()
    rating = models.IntegerField()
    review = models.CharField(max_length=500)
    dt = models.CharField(max_length=50)
    tm = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.review

class product_pic(models.Model):
    product_master_id = models.IntegerField()
    pic_path = models.CharField(max_length=350)

    def __str__(self):
        return self.product_master_id

class data_set(models.Model):
    sentiment_type = models.CharField(max_length=50)
    data_path = models.CharField(max_length=350)

    def __str__(self):
        return self.sentiment_type
