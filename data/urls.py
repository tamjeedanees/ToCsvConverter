from django.conf.urls import url

from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url('^$', views.home, name='home'),
    url('^contact/$', views.contact, name='contact'),
    url('^tag-name/$',views.tag_name, name="tag-name")

]