from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.six.moves.urllib.parse import urlsplit

from fibonacci_numbers.views import home_page
from fibonacci_numbers.models import Fibonacci, get_fibonacci_number, List


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)


class FibonacciAndListModelTest(TestCase):
    def test_saving_and_retrieving_numbers(self):
        list_ = List()
        list_.save()
        first_number = Fibonacci()
        first_number.parameter = 0
        first_number.result = str(get_fibonacci_number(0))
        first_number.list = list_
        first_number.save()

        second_number = Fibonacci()
        second_number.parameter = 1
        second_number.result = str(get_fibonacci_number(1))
        second_number.list = list_
        second_number.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_numbers = Fibonacci.objects.all()
        self.assertEqual(saved_numbers.count(), 2)

        first_saved_number = saved_numbers[0]
        second_saved_number = saved_numbers[1]
        self.assertEqual(
            first_saved_number.result, str(get_fibonacci_number(0))
        )
        self.assertEqual(first_saved_number.list, list_)
        self.assertEqual(
            second_saved_number.result, str(get_fibonacci_number(1))
        )
        self.assertEqual(second_saved_number.list, list_)


class UsersViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get('/lists/only-person/')
        self.assertTemplateUsed(response, 'list.html')

    def test_display_all_calculations(self):
        list_ = List.objects.create()
        first_result = str(get_fibonacci_number(14))
        second_result = str(get_fibonacci_number(123))

        Fibonacci.objects.create(
            parameter=14, list=list_, result=first_result
        )
        Fibonacci.objects.create(
            parameter=123, list=list_, result=second_result
        )

        response = self.client.get('/lists/only-person/')

        self.assertContains(response, first_result)
        self.assertContains(response, second_result)


class NewListTest(TestCase):
    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new', data={'new_n': 6}
        )
        self.assertEqual(Fibonacci.objects.count(), 1)
        first_result = Fibonacci.objects.first()
        self.assertEqual(first_result.result, '8')

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new', data={'new_n': 6}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            urlsplit(response['location']).path, '/lists/only-person'
        )
