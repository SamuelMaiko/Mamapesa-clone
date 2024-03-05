from datetime import date
from django.forms import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import CustomUser, TrustScore, Savings, Loan, Item, LoanItem, LoanRepayment, Transaction, SavingsItem, Withdrawal


class TestCustomUser(TestCase):
    def test_custom_user_created(self):

        user = CustomUser.objects.create(
            username='test_user', 
            password='test_password', 
        )
        # Check if the user is created successfully
        assert user.username == 'test_user'
        
        # Check if created_at and updated_at fields are set automatically
        assert user.created_at is not None
        assert user.updated_at is not None
        
        # Check if groups and permissions are set correctly
        assert user.groups.count() == 0
        assert user.user_permissions.count() == 0


class TestTrustscore(TestCase):
    def test_create_trust_score(self):
    # Create a user for testing
        user = CustomUser.objects.create(
            username='test_user', 
            password='test_password', 
            email='test@example.com'
        )
        
        # Create a TrustScore instance
        trust_score = TrustScore.objects.create(
            user=user, 
            score=80,
            is_blacklisted=False,
            comment='Test comment'
        )
        
        # Check if TrustScore instance is created successfully
        assert trust_score.user.username == 'test_user'
        assert trust_score.score == 80
        assert not trust_score.is_blacklisted
        assert trust_score.comment == 'Test comment'
        assert trust_score.timestamp is not None


class TestLoan(TestCase):
    def test_create_loan(self):
        user = CustomUser.objects.create(
            username='test_user', 
            password='password', 
            email='test@example.com'
            )
        loan = Loan.objects.create(
            user=user,
            amount=1000,
            interest_rate=5,
            duration_months=12,
            purpose='Test loan',
            collateral='Test collateral'
        )
        assert loan.user.username == 'test_user'
        assert loan.amount == 1000
        assert loan.interest_rate == 5
        assert loan.duration_months == 12
        assert loan.purpose == 'Test loan'
        assert loan.collateral == 'Test collateral'
        assert loan.is_approved == False
        assert loan.is_active == False
        assert loan.disbursed == False
        assert loan.repaid_amount == 0
        assert loan.total_paid == 0
        assert loan.overdue_amount == 0
        assert loan.penalty_rate == 0
        assert loan.installment_amount is None
        assert loan.grace_period_months == 0
        assert loan.application_date.date() == timezone.now().date()


class TestSavings(TestCase):
    def test_create_savings(self):
    # Create a user for testing
        user = CustomUser.objects.create(
            username='test_user', 
            password='test_password', 
            email='test@example.com'
        )
        
        # Create a Savings instance
        savings = Savings.objects.create(
            user=user, 
            amount_saved=500, 
            end_date=timezone.now() + timezone.timedelta(days=30),
            purpose='Test purpose',
            is_active=True,
            in_progress=True
        )
        
        # Check if Savings instance is created successfully
        assert savings.user.username == 'test_user'
        assert savings.amount_saved == 500
        assert savings.purpose == 'Test purpose'
        assert savings.is_active
        assert savings.in_progress
        assert savings.created_at is not None
        assert savings.updated_at is not None


# Tests the creation of an Item instance.
class TestItem(TestCase):
    def test_create_item(self):
        item = Item.objects.create(
            name='Test Item',
            description='Test description',
            in_stock=True
        )
        assert item.name == 'Test Item'
        assert item.description == 'Test description'
        assert item.in_stock == True
        assert str(item) == 'Test Item'


# Tests the creation of a LoanItem instance.
class LoanItemModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test data for Loan and Item models
        loan = Loan.objects.create()
        item = Item.objects.create(name="Test Item")

        # Create a LoanItem instance for testing
        cls.loan_item = LoanItem.objects.create(
            loan=loan,
            item=item,
            amount_paid=100.00,
            date_loaned=date(2024, 3, 5),
            return_date=date(2024, 3, 5),
            condition_on_return="Good condition"
        )

    def test_loan_item_fields(self):
        loan_item = self.loan_item

        # Test ForeignKey relationships
        self.assertEqual(loan_item.loan.id, Loan.objects.first().id)
        self.assertEqual(loan_item.item.name, "Test Item")

        # Test DecimalField
        self.assertEqual(loan_item.amount_paid, 100.00)

        # Test DateField
        self.assertEqual(loan_item.date_loaned, date(2024, 3, 5))
        self.assertEqual(loan_item.return_date, date(2024, 3, 5))

        # Test TextField
        self.assertEqual(loan_item.condition_on_return, "Good condition")

    def test_related_names(self):
        loan = self.loan_item.loan
        item = self.loan_item.item

        # Test related_name attributes
        self.assertIn(self.loan_item, loan.loan_items.all())
        self.assertIn(self.loan_item, item.loaned_items.all())


# class TestPayment(TestCase):
#     def test_create_payment(self):
#         # Create a CustomUser instance
#         user = CustomUser.objects.create(
#             username='test_user',
#             password='password',
#             email='test@example.com'
#         )

#         # Create a Payment
#         payment = Payment.objects.create(
#             user=user,
#             amount=100,
#             date=timezone.now(),
#             description='Test payment',
#             is_loan_payment=True,
#             payment_method='Credit card',
#             reference_number='123456'
#         )
        
#         # Assert properties of the Payment
#         self.assertEqual(payment.user, user, "User should match the created CustomUser instance")
#         self.assertEqual(payment.amount, 100, "Amount should be 100")
#         self.assertEqual(payment.description, 'Test payment', "Description should be 'Test payment'")
#         self.assertTrue(payment.is_loan_payment, "is_loan_payment should be True")
#         self.assertFalse(payment.is_savings_payment, "is_savings_payment should be False")
#         self.assertEqual(payment.payment_method, 'Credit card', "Payment method should be 'Credit card'")
#         self.assertEqual(payment.reference_number, '123456', "Reference number should be '123456'")
#         self.assertTrue(payment.is_successful, "Payment should be successful")

#         # Test the __str__ method
#         self.assertEqual(str(payment), f"Payment by {payment.user.username} on {payment.date} - Amount: {payment.amount}", "__str__ should match expected format")

class LoanRepaymentModelTest(TestCase):
    def setUp(self):
        self.loan = Loan.objects.create()

    def test_loan_repayment_creation(self):
        repayment = LoanRepayment.objects.create(
            loan=self.loan, amount_paid=500.00)
        self.assertEqual(repayment.loan, self.loan)
        self.assertEqual(repayment.amount_paid, 500.00)

    def test_loan_repayment_str_method(self):
        repayment = LoanRepayment.objects.create(
            loan=self.loan, amount_paid=500.00)
        self.assertEqual(
            str(repayment),
            f"Repayment of {repayment.amount_paid} for Loan {self.loan.id}"
        )

# Tests the creation of a Transaction instance
class TestTransaction(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username='test_user',
            password='password',
            email='test@example.com'
        )

    def test_create_transaction(self):
        # Create a Transaction
        transaction = Transaction.objects.create(
            user=self.user,
            amount=500,
            description='Test transaction',
            transaction_type='income',
            timestamp=timezone.now(),
            category='Salary',
            payment_method='Bank transfer',
            reference_number='789012'
        )

        # Assert properties of the Transaction
        self.assertEqual(transaction.user, self.user, "User should be the created CustomUser instance")
        self.assertEqual(transaction.amount, 500, "Amount should be 500")
        self.assertEqual(transaction.description, 'Test transaction', "Description should be 'Test transaction'")
        self.assertEqual(transaction.transaction_type, 'income', "Transaction type should be 'income'")
        self.assertEqual(transaction.category, 'Salary', "Category should be 'Salary'")
        self.assertEqual(transaction.payment_method, 'Bank transfer', "Payment method should be 'Bank transfer'")
        self.assertEqual(transaction.reference_number, '789012', "Reference number should be '789012'")
        self.assertTrue(transaction.is_successful, "Transaction should be successful")

        # Test the __str__ method
        self.assertEqual(str(transaction), f"Transaction by {transaction.user.username} - Amount: {transaction.amount} - Type: {transaction.transaction_type}", "__str__ should match expected format")


# Tests the creation of a SavingsItem instance.
class TestSavingsItem(TestCase):
    def test_create_savings_item(self):
        # Create a CustomUser instance
        user = CustomUser.objects.create(
            username='test_user',
            password='password',
            email='test@example.com'
        )

        # Create a Savings instance
        savings = Savings.objects.create(
            user=user,
            amount_saved=500,
            end_date=timezone.now() + timezone.timedelta(days=30),
            purpose='Test purpose',
            is_active=True,
            in_progress=True
        )

        # Create an Item instance
        item = Item.objects.create(name="Test Item")

        # Create a SavingsItem
        savings_item = SavingsItem.objects.create(
            savings=savings,
            item=item,
            target_amount=1000,
            start_date=timezone.now(),
            due_date=timezone.now() + timezone.timedelta(days=30),
            achieved=False
        )
        
        # Assert properties of the SavingsItem
        self.assertEqual(savings_item.savings, savings, "Savings should match the created Savings instance")
        self.assertEqual(savings_item.item, item, "Item should match the created Item instance")
        self.assertEqual(savings_item.target_amount, 1000, "Target amount should be 1000")
        self.assertFalse(savings_item.achieved, "Achieved should be False")

        # Test the __str__ method
        self.assertEqual(str(savings_item), f"{savings_item.item.name} for {savings_item.savings.user.username} - Target: {savings_item.target_amount}", "__str__ should match expected format")


class WithdrawalModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='password123')
        self.savings = Savings.objects.create()
        self.loan = Loan.objects.create()

    def test_withdrawal_str_method(self):
        withdrawal = Withdrawal.objects.create(
            user=self.user, amount=100.00)
        self.assertEqual(
            str(withdrawal),
            f"Withdrawal by {self.user.username} on {withdrawal.date} - Amount: {withdrawal.amount}"
        )

    def test_clean_method_with_both_savings_and_loan(self):
        with self.assertRaises(ValidationError):
            withdrawal = Withdrawal.objects.create(
                user=self.user, amount=100.00, savings=self.savings, loan=self.loan)
            withdrawal.clean()

    def test_clean_method_with_neither_savings_nor_loan(self):
        with self.assertRaises(ValidationError):
            withdrawal = Withdrawal.objects.create(
                user=self.user, amount=100.00)
            withdrawal.clean()

    def test_clean_method_with_savings_only(self):
        withdrawal = Withdrawal.objects.create(
            user=self.user, amount=100.00, savings=self.savings)
        self.assertIsNone(withdrawal.clean())

    def test_clean_method_with_loan_only(self):
        withdrawal = Withdrawal.objects.create(
            user=self.user, amount=100.00, loan=self.loan)
        self.assertIsNone(withdrawal.clean())