from django.conf.urls import include, url
from django.contrib import admin

from fibonacci_numbers import urls as fibonacci_numbers_urls

urlpatterns = [
    url(r'^$', 'fibonacci_numbers.views.home_page', name='home'),
    url(r'^lists/', include(fibonacci_numbers_urls)),

    # url(r'^admin/', include(admin.site.urls)),
]
