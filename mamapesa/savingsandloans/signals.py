from django.dispatch import receiver, Signal
# from newmamapesa.models import SavingsItem, SavingsTransaction, LoanTransaction
from newmamapesa.models import SavingsItem, Payment
from django.db.models.signals import post_save
from decimal import Decimal
from django.db.models import Q

@receiver(post_save, sender=SavingsItem)
def update_saving_account_total_amount(sender, instance, created, **kwargs):
    all_savings_items=instance.savings.savings_items.all()
    total_price=Decimal("0.00")
    for each in all_savings_items:
        total_price+=each.amount_saved
        
    instance.savings.amount_saved=total_price
    instance.savings.save()
    
# after_deposit - signal sent after a deposit is made 
after_deposit=Signal()
@receiver(after_deposit, sender=None)
def create_a_transaction(sender, **kwargs):
    customer=kwargs["user"].customer
    amount=kwargs["amount"]
    type=kwargs["type"]
    transaction_id=kwargs["transaction_id"]
    payment_method=1
    payment_ref=kwargs["payment_ref"]
    status=kwargs["status"]
    savings_item=kwargs["savings_item"]
    receiving_till=kwargs.get("receiving_till")
    
    new_payment=Payment(
        customer=customer,
        amount=amount,
        type=type,
        transaction_id=transaction_id,
        payment_method_id=payment_method,
        payment_ref=payment_ref,
        status=status,
        savings_item=savings_item,
        receiving_till=receiving_till
        )
    new_payment.save()

update_savings_payment_status=Signal()
@receiver(update_savings_payment_status, sender=None)
def update_status(sender, **kwargs):
    customer=kwargs["user"].customer
    status=kwargs["status"]
    type=kwargs["type"]
    savings_item=kwargs["savings_item"]
    
    specific_payment=Payment.objects.filter(Q(customer=customer) & Q(savings_item=savings_item) & Q(type=type)).first()
    specific_payment.status=status
    specific_payment.save()
    
    
loan_disbursed=Signal()
# @receiver(loan_disbursed, sender=None)
# def create_loan_transaction(sender, **kwargs):
#     LoanTransaction.objects.create(
#         user=kwargs["user"],
#         amount=kwargs["amount"],
#         description=f"Loan disbursed for Kshs. {kwargs['amount']}",
#         type='loan_disbursement',
#         loan=kwargs["loan"]
#     )
#     loan=kwargs["loan"]
#     loan.is_disbursed=True
#     loan.save()


after_repay_loan=Signal()
# @receiver(after_repay_loan, sender=None)
# def create_transaction_after_repay(sender, **kwargs):
#     user=kwargs["user"]
#     loan=kwargs["loan"]
#     amount=kwargs["amount"]
    
#     new_loan_transaction=LoanTransaction(user=user, loan=loan, amount=amount, type="loan_repayment")
#     new_loan_transaction.save()