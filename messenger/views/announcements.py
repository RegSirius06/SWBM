import os
import uuid

from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from messenger.models import announcement
from messenger.forms import announcements

@permission_required('bank.staff_')
@permission_required('bank.ant_edit')
def all_announcements_view(request):
    anns = announcement.objects.filter(status=False)#.order_by("creator", "name")
    paginator1 = Paginator(anns, 25)
    page1 = request.GET.get('page1')
    try:
        items1 = paginator1.page(page1)
    except PageNotAnInteger:
        items1 = paginator1.page(1)
    except EmptyPage:
        items1 = paginator1.page(paginator1.num_pages)
    return render(
        request,
        'messenger/announcements/announcements.html',
        context={'plans': items1,},
    )

@login_required
def new_announcement_add(request):
    def prov(img: str) -> bool:
        flag = True
        with os.scandir(os.path.join(settings.MEDIA_ROOT, 'announcements/')) as listOfEntries:
            for entry in listOfEntries:
                if entry.is_file():
                    if img == entry.name:
                        flag = False
                        break
        return flag

    flag = request.user.has_perm('bank.ant_edit')
    if request.method == 'POST':
        form = announcements.NewAnnouncementFullForm(request.POST, request.FILES) if flag\
                else announcements.NewAnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            plan_ = announcement()
            plan_.id = uuid.uuid4()
            plan_.name = form.cleaned_data['name']
            plan_.text = form.cleaned_data['text']
            image = form.cleaned_data['picture']
            if image:
                name = str(image.name)
                try:
                    i = 0
                    end = f".{name.split('.')[-1]}"
                    name_x = name
                    while not prov(name_x):
                        name_x = f"{'.'.join(name.split('.')[:-1])}{i}{end}"
                        i += 1
                    name = name_x
                    plan_.picture = name
                    with open(os.path.join(settings.MEDIA_ROOT, 'announcements/', name), 'wb') as file:
                        for chunk in image.chunks():
                            file.write(chunk)
                    print('ok2')
                except FileNotFoundError:
                    os.makedirs(os.path.join(settings.MEDIA_ROOT, 'announcements/'))
                    with open(os.path.join(settings.MEDIA_ROOT, 'announcements/', image.name), 'wb') as file:
                        for chunk in image.chunks():
                            file.write(chunk)
                    plan_.picture = name
                    print('ok')
            plan_.orientation = form.cleaned_data['type_']
            if announcement.objects.all().exists(): number = list(announcement.objects.all().order_by('-number'))[-1].number + 1
            else: number = 1
            plan_.number = number
            if flag: plan_.creator = form.cleaned_data['creator']
            else: plan_.creator = request.user.account
            plan_.save()
            return redirect('index_of_messenger')
    else:
        text = name = ''
        initial={'text': text, 'name': name,}
        form = announcements.NewAnnouncementFullForm(initial=initial) if flag\
                else announcements.NewAnnouncementForm(initial=initial)
    return render(
        request,
        'messenger/new_and_renew/add_new_with_files.html',
        {'form': form, 'head': "Создание нового объявления", 'name': "Подать заявку на создание",
         'foot': "После модерации объявление появится на главной странице.",}
    )

@permission_required('bank.staff_')
@permission_required('bank.ant_edit')
def re_new_announcement_add(request, pk):
    plan_ = get_object_or_404(announcement, id=pk)
    if request.method == 'POST':
        form = announcements.ReNewAnnouncementForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['delete']:
                plan_.delete()
            else:
                plan_.creator = form.cleaned_data['creator']
                plan_.status = form.cleaned_data['status']
                plan_.save()
            return redirect('anns-new')
    else:
        creator = plan_.creator
        form = announcements.ReNewAnnouncementForm(initial={'creator': creator,})
    return render(request, 'messenger/new_and_renew/edit_or_delete.html', {'form': form, 'head': 'Изменение объявления'})
