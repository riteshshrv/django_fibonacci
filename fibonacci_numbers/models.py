from django.db import models


def get_fibonacci_number(n):
    """
    Find nth fibonacci number iteratively
    """
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a


class List(models.Model):
    pass


class Fibonacci(models.Model):
    parameter = models.IntegerField(primary_key=True)
    list = models.ForeignKey(List, default=None)
    result = models.CharField(max_length=200)
