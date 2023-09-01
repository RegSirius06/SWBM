import uuid

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required

from bank.models import good
from bank.forms import goods

def shop_view(request):
    return render(
        request,
        'bank/shop/shop.html',
        context={'goods': good.objects.all()}
    )

@permission_required('bank.staff_')
@permission_required('bank.meria')
def new_good_add(request):
    if request.method == 'POST':
        form = goods.NewGoodAddForm(request.POST)
        if form.is_valid():
            good_ = good()
            good_.id = uuid.uuid4()
            good_.name = form.cleaned_data['name']
            good_.comment = form.cleaned_data['comment']
            good_.cost = int(form.cleaned_data['cost'])
            good_.save()
            return redirect('shop')
    else:
        name = comment = ''
        cost = 0
        form = goods.NewGoodAddForm(initial={'cost': cost, 'comment': comment, 'name': name,})
    return render(request, 'bank/new_and_renew/add_new.html', {'form': form, 'title': "Ассортимент магазина", 'head': "Добавить новый товар:"})

@permission_required('bank.staff_')
@permission_required('bank.meria')
def re_new_good_add(request, pk):
    good_ = get_object_or_404(good, id=pk)
    if request.method == 'POST':
        form = goods.ReNewGoodAddForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['delete']:
                good_.delete()
            else:
                good_.name = form.cleaned_data['name']
                good_.comment = form.cleaned_data['comment']
                good_.cost = int(form.cleaned_data['cost'])
                good_.save()
            return redirect('shop')
    else:
        name = good_.name
        comment = good_.comment
        cost = good_.cost
        form = goods.ReNewGoodAddForm(initial={'cost': cost, 'comment': comment, 'name': name,})
    return render(request, 'bank/new_and_renew/edit_or_delete.html', {'form': form, 'head': 'Изменение товара:', 'title': "Ассортимент магазина",})
