from django.contrib import admin
from .models import user_login,category_master,company_details,data_set,product_master,product_pic,product_review,sub_category_master
from .models import user_details

# Register your models here.
admin.site.register(user_login)
admin.site.register(category_master)
admin.site.register(company_details)
admin.site.register(data_set)
admin.site.register(product_master)
admin.site.register(product_pic)
admin.site.register(product_review)
admin.site.register(sub_category_master)
admin.site.register(user_details)
