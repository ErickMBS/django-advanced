from .actions import nfe_emitida, nfe_nao_emitida
from vendas.models import Venda, ItemDoPedido
from django.contrib import admin


class ItemPedidoInLine(admin.TabularInline):
    model = ItemDoPedido
    extra = 1


class VendaAdmin(admin.ModelAdmin):
    list_filter = ('pessoa__doc', 'desconto',)
    autocomplete_fields = ('pessoa',)
    readonly_fields = ('valor',)
    fields = ('numero', 'valor', ('desconto', 'impostos'), 'pessoa', 'nfe_emitida',)
    list_display = ('id', 'numero', 'valor', 'desconto', 'impostos', 'pessoa', 'nfe_emitida',)
    search_fields = ('pessoa__first_name', 'pessoa__last_name', 'id',)
    actions = (nfe_emitida, nfe_nao_emitida,)
    inlines = (ItemPedidoInLine,)


admin.site.register(Venda, VendaAdmin)
admin.site.register(ItemDoPedido)
