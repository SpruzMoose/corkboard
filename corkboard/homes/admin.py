from django.contrib import admin
from .models import Category, Pin, Board, PinToBoard

# Register your models here.
admin.site.register(Category)
admin.site.register(Pin)
admin.site.register(Board)

#@admin.register(PinToBoard)
#class PinToBoardAdmin(admin.ModelAdmin):
#    exclude = ('rank',)
admin.site.register(PinToBoard)
