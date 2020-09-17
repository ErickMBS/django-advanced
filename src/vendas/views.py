from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .forms import ItemPedidoForm, ItemDoPedidoModelForm
from .models import Venda, ItemDoPedido
import logging

logger = logging.getLogger('django')


class DashboardView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('vendas.ver_dashboard'):
            return HttpResponse('Acesso negado, você precisa de permissão')

        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        data = {
            'media': Venda.objects.media(),
            'media_desc': Venda.objects.media_desc(),
            'min': Venda.objects.min(),
            'max': Venda.objects.max(),
            'n_ped': Venda.objects.n_ped(),
            'n_ped_nfe': Venda.objects.n_ped_nfe()
        }

        return render(
            request, 'vendas/dashboard.html', data
        )


class NovoPedido(View):
    def get(self, request):
        return render(request, 'vendas/novo-pedido.html')

    def post(self, request):
        data = {}
        data['numero'] = request.POST['numero']
        data['desconto'] = float(str(request.POST['desconto']).replace(',', '.'))
        data['venda_id'] = request.POST['venda_id']

        if data['venda_id']:
            venda = Venda.objects.get(id=data['venda_id'])
        else:
            venda = Venda.objects.create(
                numero=data['numero'],
                desconto=data['desconto']
            )

        itens = venda.itemdopedido_set.all()
        data['venda'] = venda
        data['itens'] = itens
        data['form_item'] = ItemPedidoForm()

        return render(request, 'vendas/novo-pedido.html', data)


class NovoItemPedido(View):
    def get(self, request, pk):
        pass

    def post(self, request, venda):
        data = {}

        item = ItemDoPedido.objects.filter(produto_id=request.POST['produto_id'], venda_id=venda).first()
        if item:
            data['mensagem'] = 'Item já incluído no pedido, por favor edite o item.'
        else:
            item = ItemDoPedido.objects.create(
                produto_id=request.POST['produto_id'],
                quantidade=request.POST['quantidade'],
                desconto=request.POST['desconto'],
                venda_id=venda
            )

        data['item'] = item
        data['form_item'] = ItemPedidoForm()
        data['numero'] = item.venda.numero
        data['desconto'] = item.venda.desconto
        data['venda'] = item.venda
        data['itens'] = item.venda.itemdopedido_set.all()

        return render(request, 'vendas/novo-pedido.html', data)


class ListaVendas(View):
    def get(self, request):
        logger.debug('Acessaram a listagem de vendas')
        try:
            1/0
        except Exception as e:
            logger.error(str(e))
        vendas = Venda.objects.all()
        return render(request, 'vendas/lista-vendas.html', {'vendas': vendas})


class EditPedido(View):
    def get(self, request, venda):
        data = {}
        venda = Venda.objects.get(id=venda)
        data['form_item'] = ItemPedidoForm()
        data['numero'] = venda.numero
        data['desconto'] = float(venda.desconto)
        data['venda'] = venda
        data['itens'] = venda.itemdopedido_set.all()

        return render(request, 'vendas/novo-pedido.html', data)


class DeletePedido(View):
    def get(self, request, venda):
        venda = Venda.objects.get(id=venda)
        return render(request, 'vendas/delete-pedido-confirm.html', {'venda': venda})

    def post(self, request, venda):
        venda = Venda.objects.get(id=venda)
        venda.delete()
        return redirect('lista-vendas')


class DeleteItemPedido(View):
    def get(self, request, item):
        item_pedido = ItemDoPedido.objects.get(id=item)
        return render(request, 'vendas/delete-item-pedido-confirm.html', {'item_pedido': item_pedido})

    def post(self, request, item):
        item_pediddo = ItemDoPedido.objects.get(id=item)
        venda_id = item_pediddo.venda.id
        item_pediddo.delete()
        return redirect('edit-pedido', venda=venda_id)


class EditItemPedido(View):
    def get(self, request, item):
        item_pedido = ItemDoPedido.objects.get(id=item)
        form = ItemDoPedidoModelForm(instance=item_pedido)
        return render(request, 'vendas/edit-item-pedido.html', {'item_pedido': item_pedido, 'form': form})

    def post(self, request, item):
        item_pediddo = ItemDoPedido.objects.get(id=item)
        item_pediddo.quantidade = request.POST.get('quantidade')
        item_pediddo.desconto = request.POST.get('desconto')
        item_pediddo.save(update_fields=('quantidade', 'desconto',))

        venda_id = item_pediddo.venda.id
        return redirect('edit-pedido', venda=venda_id)
