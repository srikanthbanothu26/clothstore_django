from django.http import HttpResponse


def home(request):
    print("i am in home page")
    return HttpResponse("Hello, World!")


def second_page(request):
    print("i am in second pages ")
    return HttpResponse("Hello, World! This is the second page.")