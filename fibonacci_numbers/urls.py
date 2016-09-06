from django.conf.urls import url

urlpatterns = [
    url(r'^(\d+)/$', 'fibonacci_numbers.views.view_list', name='view_list'),
    url(r'^(\d+)/add_to_list$', 'fibonacci_numbers.views.add_to_list', name='add_to_list'),
    url(r'new', 'fibonacci_numbers.views.new_list', name='new_list'),
]
