import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from .serializers import *
from .models import *
# Create your views here.
def isValid(id):
    if id is not None:
        return True
    else:
        return False
class ListLedgers(APIView):
    def get(self,request):
        tenant_id=request.GET.get('tenant_id',None)
        if isValid(tenant_id):
            distributor_id = request.GET.get('distributor_id', None)
            store_id=request.GET.get('store_id', None)
            if isValid(distributor_id) and isValid(store_id):
                distributor_object = distributor.objects.get(distributor_id=distributor_id,tenant_id=tenant_id)
                store_object=store.objects.filter(distributor_id=distributor_object,store_id=store_id)
                serializer = StoreSerializer(store_object, many=True)
                store_details=serializer.data
                result=json.loads(json.dumps(store_details))
                for Store in result:
                    ledger_object = ledger.objects.get(distributor_id=distributor_object, store_id=Store["store_id"])
                    serializer1 = LedgerSerializer(ledger_object)
                    Store["Ledger"] = serializer1.data
                return Response(result)
            elif isValid(distributor_id) and not isValid(store_id):
                distributor_object=distributor.objects.get(distributor_id=distributor_id,tenant_id=tenant_id)
                serializer=DistributorSerializer(distributor_object)
                distributor_details=serializer.data
                store_details = json.loads(json.dumps(distributor_details["Store"]))
                for Store in store_details:
                    ledger_object = ledger.objects.get(distributor_id=distributor_object, store_id=Store["store_id"])
                    serializer1 = LedgerSerializer(ledger_object)
                    Store["Ledger"] = serializer1.data
                distributor_details['Store']=store_details
                return Response(distributor_details)
            elif not isValid(distributor_id) and isValid(store_id):
                store_object=store.objects.get(tenant_id=tenant_id,store_id=store_id)
                distributor_object=store_object.distributor_id.all()
                result={}
                for Distributor in distributor_object:
                    serializer = DistributorSerializerList(Distributor)
                    try:
                        ledger_object=ledger.objects.get(distributor_id=Distributor,store_id=store_id)
                        result[Distributor.distributor_id] = serializer.data
                        serializer1 = StoreSerializer(store_object)
                        result[Distributor.distributor_id]["Store"] = serializer1.data
                        serializer2=LedgerSerializer(ledger_object)
                        result[Distributor.distributor_id]["Store"]["Ledger"]=serializer2.data
                    except:
                        result=result
                return Response(result)
            else:
                distributor_object=distributor.objects.filter(tenant_id=tenant_id)
                result={}
                for Distributor in distributor_object:
                    serializer = DistributorSerializer(Distributor)
                    result[Distributor.distributor_id]=serializer.data
                    store_details=json.loads(json.dumps(result[Distributor.distributor_id]["Store"]))
                    for Store in store_details:
                        ledger_object = ledger.objects.filter(distributor_id=Distributor,store_id=Store["store_id"])
                        serializer1 = LedgerSerializer(ledger_object,many=True)
                        Store["Ledger"]=serializer1.data
                    result[Distributor.distributor_id]["Store"]=store_details
                return Response(result)
class EditLedger(APIView):
    def patch(self,request):
        ledger_id=request.GET.get('ledger_id',None)
        if ledger_id is not None:
            ledger_count=ledger.objects.filter(id=ledger_id).count()
            if ledger_count>0:
                ledger_queryset=ledger.objects.get(id=ledger_id)
                serializer=EditLedgerSerializer(ledger_queryset,data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    serializer1=LedgerSerializer(ledger_queryset)
                    return Response(serializer1.data)
            else:
                return Response({"ledger id not found"})
        else:
            return Response({"ledger id not found"})

class CreateLedger(APIView):
    def post(self,request):
        data=request.data #json
        tenant_id=request.GET.get('tenant_id')
        distributor_id=data['distributor_id']
        store_id=data['store_id']
        enabled = data['enabled']
        credit_rating = data['credit_rating']
        credit_limit = data['credit_limit']
        credit_balance = data['credit_balance']
        credit_outstanding = data['credit_outstanding']
        distributor_object=distributor.objects.get(distributor_id=distributor_id)
        led=ledger(tenant_id=tenant_id,distributor_id=distributor_object,store_id=store_id,enabled=enabled,credit_rating=credit_rating,credit_limit=credit_limit,credit_balance=credit_balance,
                   credit_outstanding=credit_outstanding)
        try:
            led.save()
            store_object=store.objects.get(store_id=store_id)
            store_object.distributor_id.add(distributor_object)
            return Response(request.data)
        except:
            return Response({"Already having ledger"})

class Transaction(APIView):
    def post(self,request,type):
        if type=="credit":
            ledger_id=request.data.get('id')
            transaction_amount=request.data.get('transaction_amount')
            ledger_count = ledger.objects.filter(id=ledger_id).count()
            if ledger_count>0:
                ledgers=ledger.objects.filter(id=ledger_id)
                serializer=LedgerSerializer(ledgers,many=True)
                credit_limit=serializer.data[0]["credit_limit"]
                credit_outstanding=serializer.data[0]["credit_outstanding"]
                credit_balance = serializer.data[0]["credit_balance"]

                new_balance=credit_balance+transaction_amount
                c_outstanding=0
                if credit_outstanding>=transaction_amount:
                    c_outstanding=credit_outstanding-transaction_amount
                elif credit_outstanding!=0:
                    c_outstanding =0
                for object in ledgers:
                    object.credit_balance = new_balance
                    object.credit_outstanding = c_outstanding
                    object.save()
                ledgertable=ledger_transactions(ledger_id=ledgers[0],transaction_amount=transaction_amount,credit_balance=new_balance,credit_outstanding=credit_outstanding)
                ledgertable.save()

                ledgeractionsTable= ledger_action_types(name="Credit", description="Amount credited")
                ledgeractionsTable.save()

                ledger_action_id = (ledger_action_types.objects.last()).id
                action_type_id = ledger_action_types.objects.filter(id=ledger_action_id)
                ledgeractions = ledger_actions(ledger_id=ledgers[0], action_type_id=action_type_id[0], prev_value=credit_balance,
                                    current_value=new_balance)
                ledgeractions.save()
                return Response({"Success"})
            else:
                return Response({"Ledger id not found"})

        elif type == "debit":
            ledger_id = request.data.get('id')
            transaction_amount = request.data.get('transaction_amount')
            ledger_count = ledger.objects.filter(id=ledger_id).count()
            if ledger_count > 0:
                ledgers = ledger.objects.filter(id=ledger_id)
                serializer = LedgerSerializer(ledgers, many=True)
                credit_limit = serializer.data[0]["credit_limit"]
                credit_outstanding = serializer.data[0]["credit_outstanding"]
                credit_balance = serializer.data[0]["credit_balance"]
                if transaction_amount <= credit_balance:
                    new_amount = credit_balance - transaction_amount
                    total_outstanding = credit_outstanding + transaction_amount
                    if total_outstanding <= credit_limit:
                        new_credit_outstanding = credit_outstanding + transaction_amount
                        for object in ledgers:
                            object.credit_balance = new_amount
                            object.credit_outstanding = new_credit_outstanding
                            object.save()
                        ledgerTable = ledger_transactions(ledger_id=ledgers[0], transaction_amount=transaction_amount, credit_balance=new_amount,
                                                 credit_outstanding=new_credit_outstanding)
                        ledgerTable.save()
                        ledgeractionsTable = ledger_action_types(name="Debit", description="Amount debited")
                        ledgeractionsTable.save()
                        ledger_actiontype_id = (ledger_action_types.objects.last()).id
                        action_type_id = ledger_action_types.objects.filter(id=ledger_actiontype_id)
                        ledgeractions = ledger_actions(ledger_id=ledgers[0], action_type_id=action_type_id[0], prev_value=credit_balance,
                                            current_value=new_amount)
                        ledgeractions.save()
                        return Response({"Success"})
                    else:
                        return Response({"Credit limit exceeded"})
                else:
                    return Response({"Amount not sufficient"})
            else:
                return Response({"Ledger id not found"})
