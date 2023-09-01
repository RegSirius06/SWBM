from django.shortcuts import render

def index(request):
    return render(
        request,
        'choice_of_path/index.html',
        context={},
    )

