from django.shortcuts import render


def home_page(request):
    return render(request, 'home.html', {
        'new_nth_number': request.POST.get('new_n', '')
    })
