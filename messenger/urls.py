from django.urls import re_path

from messenger.views import chats, updates, messages, announcements, view_info

urlpatterns = [
    re_path(r'^$', view_info.index, name='index_of_messenger'),
    re_path(r'^themes/$', view_info.list_themes, name='list-themes'),
    re_path(r'^messages/$', view_info.home, name='messages'),
    re_path(r'^messages/detail/(?P<pk>[-\w]+)/$', view_info.view_message_detail, name='messages-detail'),

    re_path(r'^announcement/new/$', announcements.new_announcement_add, name='anns'),
    re_path(r'^announcement/edit/$', announcements.all_announcements_view, name='anns-new'),
    re_path(r'^announcement/edit/(?P<pk>[-\w]+)/$', announcements.re_new_announcement_add, name='anns-new-n'),

    re_path(r'^messages/new/$', messages.new_message_add, name='messages-new'),
    re_path(r'^messages/edit/$', messages.home_send, name='messages-edit'),
    re_path(r'^messages/edit/(?P<pk>[-\w]+)/$', messages.re_new_message_add, name='messages-edit-n'),

    re_path(r'^messages/resend/(?P<chat_id>[-\w]+)/(?P<message_id>[-\w]+)/$', messages.message_resend, name='messages-resend'),

    re_path(r'^chats/new/$', chats.new_chat_add, name='chats-new'),
    re_path(r'^chats/new/conflict/(?P<new_chat_id>[-\w]+)/(?P<new_message_id>[-\w]+)/(?P<new_chat_valid_id>[-\w]+)/(?P<existing_chat_id>[-\w]+)/$',
            chats.new_chat_add_confilct, name='chats-new-conflict'),
    re_path(r'^chats/archive/$', chats.chat_archive, name='chats-archived'),
    re_path(r'^chats/archive/(?P<pk>[-\w]+)/$', chats.chat_archived_view, name='chats-archived-n'),
    re_path(r'^chats/(?P<pk>[-\w]+)/$', chats.chat_view, name='chats-n'),
    re_path(r'^chats/(?P<pk>[-\w]+)/edit/$', chats.re_new_chat_add, name='chats-edit-n'),
    
    re_path(r'update/messages/(?P<pk>[-\w]+)/', updates.update_msgs, name='update-messages'),
    re_path(r'update/chats/', updates.update_chats, name='update-chats'),
    re_path(r'update/globals/', updates.update_globals, name='update-globals'),
]