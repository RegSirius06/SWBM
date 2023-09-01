import datetime
import uuid

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required

from bank.models import plan
from bank.forms import plans

def plan_x(request):
    return render(
        request,
        'bank/plan/plan.html',
        context={'plan': plan.objects.all(),},
    )

@permission_required('bank.staff_')
@permission_required('bank.meria')
def new_plan_add(request):
    if request.method == 'POST':
        form = plans.NewPlanAddForm(request.POST)
        if form.is_valid():
            plan_ = plan()
            plan_.id = uuid.uuid4()
            plan_.time = form.cleaned_data['time']
            plan_.comment = form.cleaned_data['comment']
            plan_.number = int(form.cleaned_data['number'])
            plan_.save()
            return redirect('plans')
    else:
        time = ':'.join(f'{datetime.time(hour=datetime.datetime.today().hour, minute=datetime.datetime.today().minute)}'.split(':')[:-1])
        comment = ''
        if plan.objects.all().exists(): number = list(plan.objects.all().order_by('-number'))[-1].number + 1
        else: number = 1
        form = plans.NewPlanAddForm(initial={'number': number, 'comment': comment, 'time': time,})
    return render(request, 'bank/new_and_renew/add_new.html', {'form': form, 'title': "Расписание", 'head': "Добавление нового пункта расписания:"})

@permission_required('bank.staff_')
@permission_required('bank.meria')
def re_new_plan_add(request, pk):
    plan_ = get_object_or_404(plan, id=pk)
    if request.method == 'POST':
        form = plans.ReNewPlanAddForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['delete']:
                plan_.delete()
            else:
                plan_.time = form.cleaned_data['time']
                plan_.comment = form.cleaned_data['comment']
                plan_.number = int(form.cleaned_data['number'])
                plan_.save()
            return redirect('plans')
    else:
        time = plan_.time
        comment = plan_.comment
        number = plan_.number
        form = plans.ReNewPlanAddForm(initial={'number': number, 'comment': comment, 'time': time,})
    return render(request, 'bank/new_and_renew/edit_or_delete.html', {'form': form, 'head': 'Изменение пункта расписания:', 'title': "Расписание"})
