from django.db.models.signals import post_save
from django.dispatch import receiver
from clientes.models import Person
from django.db import models
from produtos.models import Produto
from django.db.models import Sum, F, FloatField
from .managers import VendaManager


class Venda(models.Model):
    numero = models.CharField(max_length=7)
    valor = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True)
    impostos = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=0)
    pessoa = models.ForeignKey(Person, null=True, blank=True, on_delete=models.CASCADE)
    nfe_emitida = models.BooleanField(default=False)

    objects = VendaManager()

    class Meta:
        permissions = (
            ('setar_nfe', 'Usuario pode alterar parametro NF-e'),
            ('ver_dashboard', 'Pode visualizar o Dashboard'),
            ('permissao3', 'Permissão 3'),
        )

    def calcular_total(self):
        tot = self.itemdopedido_set.all().aggregate(
            tot_ped=Sum((F('quantidade') * F('produto__preco')) - F('desconto'), output_field=FloatField())
        )['tot_ped'] or 0

        tot = tot - float(self.impostos) - float(self.desconto)
        self.valor = tot
        Venda.objects.filter(id=self.id).update(valor=tot)

    def __str__(self):
        return self.numero


class ItemDoPedido(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.FloatField()
    desconto = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    class Meta:
        verbose_name_plural = 'Itens do Pedido'

    def __str__(self):
        return f'Venda: {self.venda.numero} | Produto: {self.produto.descricao} | Qtd: {self.quantidade}'


@receiver(post_save, sender=ItemDoPedido)
def update_vendas_total_from_item(sender, instance, **kwargs):
    instance.venda.calcular_total()


@receiver(post_save, sender=Venda)
def update_vendas_total(sender, instance, **kwargs):
    instance.calcular_total()
