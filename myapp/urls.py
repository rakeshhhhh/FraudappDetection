"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('home', views.home, name='home'),
    path('contactus', views.contactus, name='contactus'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('admin_settings', views.admin_settings, name='admin_settings'),
    path('admin_settings_404', views.admin_settings_404, name='admin_settings_404'),
    path('admin_changepassword', views.admin_changepassword, name='admin_changepassword'),

    path('admin_category_master_add', views.admin_category_master_add, name='admin_category_master_add'),
    path('admin_category_master_view', views.admin_category_master_view, name='admin_category_master_view'),
    path('admin_category_master_delete', views.admin_category_master_delete, name='admin_category_master_delete'),

    path('admin_data_set_add', views.admin_data_set_add, name='admin_data_set_add'),
    path('admin_data_set_view', views.admin_data_set_view, name='admin_data_set_view'),
    path('admin_data_set_delete', views.admin_data_set_delete, name='admin_data_set_delete'),

    path('admin_company_details_view', views.admin_company_details_view, name='admin_company_details_view'),

    path('admin_company_product_master_view', views.admin_company_product_master_view, name='admin_company_product_master_view'),
    path('admin_company_product_pic_view', views.admin_company_product_pic_view, name='admin_company_product_pic_view'),

    path('admin_subcategory_master_add', views.admin_subcategory_master_add, name='admin_subcategory_master_add'),
    path('admin_subcategory_master_view', views.admin_subcategory_master_view, name='admin_subcategory_master_view'),
    path('admin_subcategory_master_delete', views.admin_subcategory_master_delete, name='admin_subcategory_master_delete'),

    path('company_login', views.company_login_check, name='company_login'),
    path('company_logout', views.company_logout, name='company_logout'),
    path('company_home', views.company_home, name='company_home'),
    path('company_details_add', views.company_details_add, name='company_details_add'),
    path('company_settings', views.company_settings, name='company_settings'),
    path('company_changepassword', views.company_changepassword, name='company_changepassword'),

    path('company_product_master_add', views.company_product_master_add, name='company_product_master_add'),
    path('company_product_master_delete', views.company_product_master_delete, name='company_product_master_delete'),
    path('company_product_master_view', views.company_product_master_view,name='company_product_master_view'),

    path('company_product_pic_add', views.company_product_pic_add, name='company_product_pic_add'),
    path('company_product_pic_delete', views.company_product_pic_delete, name='company_product_pic_delete'),
    path('company_product_pic_view', views.company_product_pic_view, name='company_product_pic_view'),

    path('company_product_review_view', views.company_product_review_view, name='company_product_review_view'),

    path('user_login', views.user_login_check, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('user_home', views.user_home, name='user_home'),
    path('user_details_add', views.user_details_add, name='user_details_add'),
    path('user_details_edit', views.user_details_edit, name='user_details_edit'),

    path('user_settings', views.user_settings, name='user_settings'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('user_changepassword', views.user_changepassword, name='user_changepassword'),

    path('user_product_master_view', views.user_product_master_view, name='user_product_master_view'),

    path('user_product_pic_view', views.user_product_pic_view, name='user_product_pic_view'),

    path('user_product_review_add', views.user_product_review_add, name='user_product_review_add'),
    path('user_product_review_delete', views.user_product_review_delete, name='user_product_review_delete'),
    path('user_product_review_view', views.user_product_review_view, name='user_product_review_view'),
    path('user_product_allreview_view', views.user_product_allreview_view, name='user_product_allreview_view'),

    path('user_product_search', views.user_product_search, name='user_product_search'),
]
