from django.shortcuts import render
from django.urls import reverse_lazy

class alink():
    def __init__(self, *args, **kwargs):
        link = kwargs.pop('link', None)
        text = kwargs.pop('text', None)
        super(alink, self).__init__(*args, **kwargs)
        if link:
            self.link = reverse_lazy(link)
            self.text = text if text else link

    link = ""
    text = ""

def render_error(request, what_app: str, error_name: str, text: str, links: list):
    list_alinks = []
    for i in links:
        list_alinks.append(alink(link=i[0], text=i[1]))
    return render(
        request,
        f'{what_app}/error_template.html',
        context={'error_name': error_name, 'text': text, 'links': list_alinks,}
    )
