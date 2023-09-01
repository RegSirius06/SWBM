from django.urls import re_path
from bank.views import plans, daily_answers, goods, accounts, view_info, transactions
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

    re_path(r'^account/create/$', accounts.new_account_add, name='index_of_messenger'),
]

"""
    re_path(r'^messages/$', views.home, name='messages'),
    re_path(r'^messages/new/$', views.new_message_add, name='messages-new'),
    re_path(r'^messages/edit/$', views.home_send, name='messages-edit'),
    re_path(r'^messages/edit/(?P<pk>[-\w]+)/$', views.re_new_message_add, name='messages-edit-n'),

    re_path(r'^chats/new/$', views.new_chat_add, name='chats-new'),
    re_path(r'^chats/new/conflict/(?P<new_chat_id>[-\w]+)/(?P<new_message_id>[-\w]+)/(?P<new_chat_valid_id>[-\w]+)/(?P<existing_chat_id>[-\w]+)/$',
            views.new_chat_add_confilct, name='chats-new-conflict'),
    re_path(r'^chats/archive/$', views.chat_archive, name='chats-archived'),
    re_path(r'^chats/archive/(?P<pk>[-\w]+)/$', views.chat_archived_view, name='chats-archived-n'),
    re_path(r'^chats/(?P<pk>[-\w]+)/$', views.chat_view, name='chats-n'),
    re_path(r'^chats/(?P<pk>[-\w]+)/edit/$', views.re_new_chat_add, name='chats-edit-n'),
"""