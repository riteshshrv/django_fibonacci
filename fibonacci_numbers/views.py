from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound

from fibonacci_numbers.models import Fibonacci, get_fibonacci_number, List


def find_or_create_nth_number(n, list_=None):
    query_set = {'parameter': n}
    if list_:
        query_set.update({'list': list_})
    try:
        result = Fibonacci.objects.get(**query_set)
    except ObjectDoesNotExist:
        result = str(get_fibonacci_number(n))
        list_ = list_ or List.objects.create()
        result = Fibonacci(parameter=n, list=list_, result=result)
        result.save()
    return result.result, list_

def home_page(request):
    return render(request, 'home.html')

def view_list(request, list_id):
    try:
        list_ = List.objects.get(id=list_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('List with id %s was not found' % list_id)
    else:
        numbers = Fibonacci.objects.filter(list=list_).order_by('-parameter')[:10]
        return render(request, 'list.html', {'list': list_})

def new_list(request):
    try:
        n = int(request.POST.get('new_n'))
    except Exception:
        # POST request made without any number
        # TODO: make custom page for 404 or override
        # the view middleware => return Http404
        return HttpResponseNotFound('Please enter a valid integer')
    else:
        nth_number, list_ = find_or_create_nth_number(n)

    return redirect('/lists/%d' % list_.id)

def add_to_list(request, list_id):
    try:
        list_ = List.objects.get(id=list_id)
    except DoesNotExist:
        return HttpResponseNotFound('List with id %s was not found' % list_id)

    try:
        n = int(request.POST.get('new_n'))
    except Exception:
        # POST request made without any number
        # TODO: make custom page for 404 or override
        # the view middleware => return Http404
        return HttpResponseNotFound('Please enter a valid integer')
    else:
        find_or_create_nth_number(n, list_)

    return redirect('/lists/%d' % list_.id)
