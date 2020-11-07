import random


def generate_code(length=10):
    """ Generate a registration random code to send by mail """
    numbers = '0123456789'
    return ''.join(random.choice(numbers) for i in range(length))