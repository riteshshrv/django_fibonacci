from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'fibonacci_numbers.views.home_page', name='home'),
    url(r'^lists/only-person/$', 'fibonacci_numbers.views.view_list', name='view_list'),
    url(r'lists/new', 'fibonacci_numbers.views.new_list', name='new_list')
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
]
