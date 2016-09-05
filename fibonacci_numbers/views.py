from django.shortcuts import render
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from fibonacci_numbers.models import Fibonacci, get_fibonacci_number


def home_page(request):
    result = None
    if request.method == 'POST':
        try:
            n = int(request.POST.get('new_n'))
        except Exception:
            # POST request made without any number
            # TODO: make custom page for 404 or override
            # the view middleware => return Http404
            pass
        else:
            try:
                result = Fibonacci.objects.get(pk=n)
            except ObjectDoesNotExist:
                result = str(get_fibonacci_number(n))
                result = Fibonacci(n, result)
                result.save()

    return render(request, 'home.html', {
        'new_nth_number': result and result.result or ''
    })