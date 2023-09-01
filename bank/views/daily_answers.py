import uuid

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required

from bank.models import daily_answer
from bank.forms import daily_answers

def answers(request):
    return render(
        request,
        'bank/daily_answers/answers.html',
        context={'answers': daily_answer.objects.all(),}
    )

@permission_required('bank.staff_')
@permission_required('bank.meria')
def new_daily_answer_add(request):
    if request.method == 'POST':
        form = daily_answers.NewDailyAnswerAddForm(request.POST)
        if form.is_valid():
            daily_answer_ = daily_answer()
            daily_answer_.id = uuid.uuid4()
            daily_answer_.name = form.cleaned_data['name']
            daily_answer_.text = form.cleaned_data['comment']
            daily_answer_.cnt = int(form.cleaned_data['cost'])
            daily_answer_.status = form.cleaned_data['giga_ans']
            daily_answer_.save()
            return redirect('answers')
    else:
        name = comment = ''
        cost = 0
        giga_ans = False
        form = daily_answers.NewDailyAnswerAddForm(initial={'cost': cost, 'comment': comment, 'name': name, 'giga_ans': giga_ans,})
    return render(request, 'bank/new_and_renew/add_new.html', {'form': form, 'title': "Задачи", 'head': "Добавление новой задачи:"})

@permission_required('bank.staff_')
@permission_required('bank.meria')
def re_new_daily_answer_add(request, pk):
    daily_answer_ = get_object_or_404(daily_answer, id=pk)
    if request.method == 'POST':
        form = daily_answers.ReNewDailyAnswerAddForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['delete']:
                daily_answer_.delete()
            else:
                daily_answer_.name = form.cleaned_data['name']
                daily_answer_.text = form.cleaned_data['comment']
                daily_answer_.cnt = int(form.cleaned_data['cost'])
                daily_answer_.status = form.cleaned_data['giga_ans']
                daily_answer_.save()
            return redirect('answers')
    else:
        name = daily_answer_.name
        comment = daily_answer_.text
        cost = daily_answer_.cnt
        giga_ans = daily_answer_.status
        form = daily_answers.ReNewDailyAnswerAddForm(initial={'cost': cost, 'comment': comment, 'name': name, 'giga_ans': giga_ans,})
    return render(request, 'bank/new_and_renew/edit_or_delete.html', {'form': form, 'title': "Задачи", 'head': "Изменение задачи:"})
