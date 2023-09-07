from django.contrib import admin
from messenger.models import message, chat, chat_and_acc, chat_valid, announcement

@admin.register(announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_filter = ["creator"]

@admin.register(chat)
class ChatAdmin(admin.ModelAdmin):
    pass

@admin.register(chat_valid)
class ChatValidAdmin(admin.ModelAdmin):
    pass

@admin.register(chat_and_acc)
class ChatAndAccAdmin(admin.ModelAdmin):
    pass

@admin.register(message)
class MessageAdmin(admin.ModelAdmin):
    list_filter = ["date", "receiver", "creator"]
