from django.contrib import admin
from bank.models import account, transaction, autotransaction, rools, good, plan, daily_answer

@admin.register(account)
class AccountAdmin(admin.ModelAdmin):
    list_filter = ["user_group", "party"]
    list_display = ('last_name', 'first_name', 'middle_name', 'party', 'user_group',)
    search_fields = ("last_name__startswith", )

@admin.register(daily_answer)
class AnswerAdmin(admin.ModelAdmin):
    pass

@admin.register(plan)
class PlanAdmin(admin.ModelAdmin):
    pass

@admin.register(transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_filter = ["date", "receiver", "creator", "history", "counted"]
    pass

@admin.register(autotransaction)
class AutoTransactionAdmin(admin.ModelAdmin):
    list_filter = ["creator", "history"]
    pass

@admin.register(good)
class GoodAdmin(admin.ModelAdmin):
    pass

@admin.register(rools)
class RoolsAdmin(admin.ModelAdmin):
    pass