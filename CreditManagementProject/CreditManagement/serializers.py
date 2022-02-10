from rest_framework import serializers
from .models import  *
class EditLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model=ledger
        fields=('enabled','credit_rating','credit_limit')
class LedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model=ledger
        fields=['id','enabled','credit_rating','credit_limit','credit_balance','credit_outstanding']
class StoreSerializer(serializers.ModelSerializer):
    #groups = LedgerSerializer(source='group_set')
    class Meta:
        model=store
        fields=('store_id','name','owner_name')
class DistributorSerializer(serializers.ModelSerializer):
    Store=StoreSerializer(read_only=True,many=True)
    class Meta:
        model=distributor
        fields=['distributor_id','name','Store']
class DistributorSerializerList(serializers.ModelSerializer):
    class Meta:
        model=distributor
        fields=['distributor_id','name']