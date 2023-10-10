from django.test import TestCase
from django.urls import reverse
from .models import CashFlow, Asset, Liability
from .forms import CashFlowForm, AssetForm, LiabilityForm


class ImportCashFlowTestCase(TestCase):
    def test_import_cash_flow_view(self):
        # Create a test CashFlowForm instance with sample data
        sample_data = {'date': '2023-09-28', 'amount': '1000.00'}
        form = CashFlowForm(data=sample_data)

        # Check if the form data is valid
        self.assertTrue(form.is_valid())

        # Send a POST request to the import_cash_flow view
        response = self.client.post(reverse('import_cash_flow'), data=sample_data, follow=True)

        # Check if the view returns a successful response (status code 200)
        self.assertEqual(response.status_code, 200)

        # Check if a CashFlow object was created in the database
        self.assertTrue(CashFlow.objects.exists())


class ImportAssetTestCase(TestCase):
    def test_import_asset_view(self):
        # Create a test AssetForm instance with sample data
        sample_data = {'name': 'Sample Asset', 'value': '50000.00'}
        form = AssetForm(data=sample_data)

        # Check if the form data is valid
        self.assertTrue(form.is_valid())

        # Send a POST request to the import_asset view
        response = self.client.post(reverse('import_asset'), data=sample_data, follow=True)

        # Check if the view returns a successful response (status code 200)
        self.assertEqual(response.status_code, 200)

        # Check if an Asset object was created in the database
        self.assertTrue(Asset.objects.exists())


class ImportLiabilityTestCase(TestCase):
    def test_import_liability_view(self):
        # Create a test LiabilityForm instance with sample data
        sample_data = {'name': 'Sample Liability', 'amount': '20000.00'}
        form = LiabilityForm(data=sample_data)

        # Check if the form data is valid
        self.assertTrue(form.is_valid())

        # Send a POST request to the import_liability view
        response = self.client.post(reverse('import_liability'), data=sample_data, follow=True)

        # Check if the view returns a successful response (status code 200)
        self.assertEqual(response.status_code, 200)

        # Check if a Liability object was created in the database
        self.assertTrue(Liability.objects.exists())
