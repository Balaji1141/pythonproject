from django.db import models

# Create your models here.
class distributor(models.Model):
    distributor_id=models.CharField(max_length=100,null=True)
    tenant_id = models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.distributor_id
class store(models.Model):
    store_id= models.CharField(max_length=100)
    distributor_id = models.ManyToManyField(distributor,null=True,related_name='Store')
    tenant_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    owner_name=models.CharField(max_length=100)
    def __str__(self):
        return self.store_id
class ledger(models.Model):
    tenant_id=models.CharField(max_length=100)
    distributor_id=models.ForeignKey(distributor,on_delete=models.CASCADE)
    store_id=models.CharField(max_length=100)
    enabled=models.BooleanField()
    credit_rating=models.IntegerField()
    credit_limit=models.PositiveIntegerField()
    credit_balance=models.PositiveIntegerField()
    credit_outstanding=models.PositiveIntegerField()

    class Meta:
        unique_together=("distributor_id","store_id")
    def __str__(self):
        return str(self.id)
class ledger_transactions(models.Model):
    ledger_id=models.ForeignKey(ledger,on_delete=models.CASCADE)
    transaction_amount=models.PositiveIntegerField()
    credit_balance=models.PositiveIntegerField()
    credit_outstanding=models.PositiveIntegerField()
    def __str__(self):
        return str(self.ledger_id)
class ledger_action_types(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    def __str__(self):
        return str(self.id)
class ledger_actions(models.Model):
    ledger_id = models.ForeignKey(ledger,on_delete=models.CASCADE)
    action_type_id=models.ForeignKey(ledger_action_types,on_delete=models.CASCADE)
    prev_value=models.PositiveIntegerField()
    current_value=models.PositiveIntegerField()
    def __str__(self):
        return str(self.ledger_id)