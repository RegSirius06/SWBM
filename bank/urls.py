from django.urls import re_path
from bank.views import autotransactions, plans, daily_answers, goods, accounts, view_info, transactions
#from django.conf.urls import url

urlpatterns = [
    re_path(r'^$', view_info.index, name='index_of_bank'),
    re_path(r'^rules/$', view_info.rools_view, name='rules'),

    re_path(r'^shop/$', goods.shop_view, name='shop'),
    re_path(r'^shop/goods/new/$', goods.new_good_add, name='good-new'),
    re_path(r'^shop/goods/edit/(?P<pk>[-\w]+)$', goods.re_new_good_add, name='good-renew'),

    re_path(r'^plan/$', plans.plan_x, name='plans'),
    re_path(r'^plan/new/$', plans.new_plan_add, name='plans-new'),
    re_path(r'^plan/edit/(?P<pk>[-\w]+)$', plans.re_new_plan_add, name='plans-renew'),

    re_path(r'^daily_answers/$', daily_answers.answers, name='answers'),
    re_path(r'^daily_answers/new/$', daily_answers.new_daily_answer_add, name='answers-new'),
    re_path(r'^daily_answers/edit/(?P<pk>[-\w]+)$', daily_answers.re_new_daily_answer_add, name='answers-renew'),

    re_path(r'^transactions/info/$', transactions.all_transactions_view, name='info-staff'),
    re_path(r'^transactions/delete/$', transactions.undo_transaction, name='undo'),
    re_path(r'^transactions/update/$', transactions.renew_transaction, name='do'),
    re_path(r'^transactions/edit/(?P<pk>[-\w]+)/$', transactions.re_new_transaction_add, name='transaction-edit'),
    
    re_path(r'^transactions/create/$', transactions.new_transaction_base_add, name='new-transaction-base'),
    re_path(r'^transactions/create/staff/$', transactions.new_transaction_staff_add, name='new-transaction-staff'),
    re_path(r'^transactions/create/full/$', transactions.new_transaction_full_add, name='new-transaction-full'),
    re_path(r'^transactions/create/buy/$', transactions.new_transaction_buy_add, name='new-transaction-buy'),
    re_path(r'^transactions/create/party/$', transactions.new_transaction_staff_party_add, name='new-transaction-party'),

    re_path(r'^transactions/my/$', view_info.my_transaction_view, name='my-transactions'),
    re_path(r'^accounts/$', view_info.all_accounts_list_view, name='accounts'),
    re_path(r'^transactions/(?P<pk>[-\w]+)/$', view_info.all_accounts_detail_view, name='account-detail'),

    re_path(r'^account/info/$', accounts.account_info, name='info-users'),
    re_path(r'^account/create/$', accounts.new_account_add, name='new-user'),
    re_path(r'^account/create/custom/$', accounts.new_account_full_add, name='new-user-custom'),
    re_path(r'^account/create/auto/$', accounts.new_account_add_from_file, name='new-user-auto'),
    re_path(r'^account/edit/all_pass/$', accounts.update_all_pass, name='update-all-pass'),
    re_path(r'^account/edit/(?P<pk>[-\w]+)/$', accounts.re_new_account_full_add, name='account-edit-n'),

    re_path(r'^autotransactions/info/$', autotransactions.all_autotransactions_view, name='autotransactions'),
    re_path(r'^autotransactions/create/$', autotransactions.new_autotransaction_add, name='new-autotransaction'),
    re_path(r'^autotransactions/edit/(?P<pk>[-\w]+)/$', autotransactions.re_new_autotransaction_add, name='autotransaction-edit'),
]