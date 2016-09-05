from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from fibonacci_numbers.views import home_page
from fibonacci_numbers.models import Fibonacci, get_fibonacci_number


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['new_n'] = 6

        response = home_page(request)

        # This is the first request so a record should've been created
        self.assertEqual(Fibonacci.objects.count(), 1)
        new_nth_number = Fibonacci.objects.first()
        self.assertEqual(new_nth_number.result, '8')

        # self.assertIn('8', response.content.decode())
        # expected_html = render_to_string('home.html', {'new_nth_number': 8})
        # self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_displays_all_calculations(self):
        Fibonacci.objects.create(
            parameter=1, result=str(get_fibonacci_number(1))
        )
        Fibonacci.objects.create(
            parameter=6, result=str(get_fibonacci_number(6))
        )
        import pdb; pdb.set_trace()
        request = HttpRequest()
        response = home_page(request)

        self.assertIn('1', response.content.decode())
        self.assertIn('8', response.content.decode())


    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['new_n'] = 6

        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_home_page_creates_record_only_when_necessary(self):
        """
        If a POST request is made without any number then
        (at least for now) a GET request is rendered
        """
        request = HttpRequest()
        request.method = 'POST'

        response = home_page(request)

        # No numbers were give in the input tag so, no records
        # should be created
        self.assertEqual(Fibonacci.objects.count(), 0)

        # self.assertIn('8', response.content.decode())
        expected_html = render_to_string('home.html', {'new_nth_number': ''})
        self.assertEqual(response.content.decode(), expected_html)


class FibonacciModel(TestCase):
    def test_saving_and_retrieving_numbers(self):
        first_number = Fibonacci()
        first_number.parameter = 0
        first_number.result = str(get_fibonacci_number(0))
        first_number.save()

        second_number = Fibonacci()
        second_number.parameter = 1
        second_number.result = str(get_fibonacci_number(1))
        second_number.save()

        saved_numbers = Fibonacci.objects.all()
        self.assertEqual(saved_numbers.count(), 2)

        first_saved_number = saved_numbers[0]
        second_saved_number = saved_numbers[1]
        self.assertEqual(
            first_saved_number.result, str(get_fibonacci_number(0))
        )
        self.assertEqual(
            second_saved_number.result, str(get_fibonacci_number(1))
        )
