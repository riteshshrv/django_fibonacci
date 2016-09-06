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


class ListsViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % list_.id)
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_numbers_only_for_that_list(self):
        correct_list = List.objects.create()
        first_result = str(get_fibonacci_number(14))
        second_result = str(get_fibonacci_number(123))
        Fibonacci.objects.create(
            parameter=14, list=correct_list, result=first_result
        )
        Fibonacci.objects.create(
            parameter=123, list=correct_list, result=second_result
        )

        other_list = List.objects.create()
        third_result = str(get_fibonacci_number(76))
        fourth_result = str(get_fibonacci_number(67))
        Fibonacci.objects.create(
            parameter=76, list=other_list, result=third_result
        )
        Fibonacci.objects.create(
            parameter=67, list=other_list, result=fourth_result
        )

        response = self.client.get('/lists/%d/' % correct_list.id)

        self.assertContains(response, first_result)
        self.assertContains(response, second_result)
        self.assertNotContains(response, third_result)
        self.assertNotContains(response, fourth_result)

    def test_passes_correct_list_to_html(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()
        response = self.client.get('/lists/%d/' % correct_list.id)
        self.assertEqual(response.context['list'], correct_list)


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

        new_list = List.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            urlsplit(response['location']).path, '/lists/%d' % new_list.id
        )


class NewItemTest(TestCase):
    def test_can_save_a_POST_requst_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/add_to_list' % correct_list.id,
            data={'new_n': 6}
        )

        self.assertEqual(Fibonacci.objects.count(), 1)
        new_number = Fibonacci.objects.first()
        self.assertEqual(new_number.result, '8')
        self.assertEqual(new_number.list, correct_list)

    def test_redirects_to_list_view(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/add_to_list' % correct_list.id,
            data={'new_n': 6}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            urlsplit(response['location']).path, '/lists/%d' % correct_list.id
        )
