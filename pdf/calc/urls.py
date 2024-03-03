from django.urls import path
from . import views
from django.conf.urls import url
from django.views.static import serve
from pdf import settings
urlpatterns =[
    path('home/Charity', views.predict_price, name='predict_price'),
    path('',views.log,name='log'),
    path('register/',views.reg,name='reg'),
    path('home/',views.home,name='home'),
    path('home/DonorHomePage',views.DonorHomePage,name='DonorHomePage'),
    path('home/DonorLogin',views.DonorLogin,name='DonorLogin'),
    path('home/About', views.About, name='About'),
    path('home/Charity', views.Charity, name='Charity'),
    path('logout', views.logout_request, name="logout"),
    path('home/change', views.change, name="change"),
    path('home/Contact', views.Contact, name="Contact"),
]