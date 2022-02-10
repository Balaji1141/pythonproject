from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(ledger)
admin.site.register(ledger_transactions)
admin.site.register(ledger_actions)
admin.site.register(ledger_action_types)
admin.site.register(distributor)
admin.site.register(store)