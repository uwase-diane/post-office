from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login_view),
    path('sign-in', views.sign_in),
    path('register', views.register_view),
    path('sign-up', views.sign_up),
    path('logout', views.logout_view),
    path('users', views.get_users),
    path('profile', views.view_profile),
    path('update-profile', views.update_profile),
    path('send-mail', views.add_mail_page),
    path('add-mail', views.add_parcel),
    path('tracking', views.tracking),
    path('addresses', views.addresses_page),
    path('add-address', views.add_address),
    path('make-address-default/<slug:address_id>', views.address_default),
    path('delete-address/<slug:address_id>', views.address_delete),
    path('parcels/<slug:parcel_id>', views.parcel_detail),
    path('parcel-payment/<slug:parcel_id>', views.parcel_payment),
    path('add-user', views.add_user),
    path('reports', views.get_reports),
]
