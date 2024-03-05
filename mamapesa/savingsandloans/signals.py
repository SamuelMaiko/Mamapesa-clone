from django.dispatch import receiver, Signal
from newmamapesa.models import SavingsItem, SavingsTransaction
from django.db.models.signals import post_save
from decimal import Decimal

@receiver(post_save, sender=SavingsItem)
def update_saving_account_total_amount(sender, instance, created, **kwargs):
    # if created:
    all_savings_items=instance.savings.savings_items.all()
    total_price=Decimal("0.00")
    for each in all_savings_items:
        total_price+=each.amount_saved
        
    instance.savings.amount_saved=total_price
    # print(f"done {total_price}")
    instance.savings.save()
    
    
# after_deposit - signal sent after a deposit is made 
after_deposit=Signal()
    
@receiver(after_deposit)
def create_a_transaction(sender, **kwargs):
    amount=kwargs["amount"]
    savings_item=kwargs["savings_item"]
    payment_method=kwargs["payment_method"]
    type=kwargs["type"]
    
    # print(type)
    new_transaction=SavingsTransaction(amount=amount, savings_item_id=savings_item, payment_method_id=payment_method, type=type)
    new_transaction.save()
    
    
    
        