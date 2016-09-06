from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from fibonacci_numbers.models import Fibonacci, get_fibonacci_number, List


def find_or_create_nth_number(n):
    try:
        result = Fibonacci.objects.get(pk=n)
    except ObjectDoesNotExist:
        result = str(get_fibonacci_number(n))
        list_ = List.objects.create()
        result = Fibonacci(parameter=n, list=list_, result=result)
        result.save()
    return result.result

def home_page(request):
    return render(request, 'home.html')

def view_list(request):
    numbers = Fibonacci.objects.all().order_by('-parameter')[:10]
    return render(request, 'list.html', {'numbers': numbers})

def new_list(request):
    try:
        n = int(request.POST.get('new_n'))
    except Exception:
        # POST request made without any number
        # TODO: make custom page for 404 or override
        # the view middleware => return Http404
        pass
    else:
        find_or_create_nth_number(n)

    return redirect('/lists/only-person')
