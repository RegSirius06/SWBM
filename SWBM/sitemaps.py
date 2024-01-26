from django.contrib import sitemaps
from django.urls import reverse

from bank.urls import urlpatterns as urlpatterns_bank
from messenger.urls import urlpatterns as urlpatterns_messenger
from choice_of_path.urls import urlpatterns as urlpatterns_COP

class MySiteMap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        l = []
        from SWBM.urls import urlpatterns as urlpatterns_
        for i in urlpatterns_:
            try: x = i.name
            except: continue
            l.append(x)
        for i in urlpatterns_COP:
            x = i.name
            l.append(x)
        for i in urlpatterns_bank:
            x = i.name
            l.append(x)
        for i in urlpatterns_messenger:
            x = i.name
            l.append(x)
        return [x for x in l if x]

    def location(self, item):
        try:
            return reverse(item)
        except Exception as e:
            tur = ("__any_id__",)
            while(True):
                try:
                    return reverse(item, args=tur)
                except:
                    tur = tuple([[x for x in tur][0]] * (len(tur) + 1))
