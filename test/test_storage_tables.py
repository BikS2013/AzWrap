import sys
import os
import pytest
import pandas as pd

# Add parent directory to path to import AzWrap
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from AzWrap.wrapper import Identity, Subscription, ResourceGroup

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

AZURE_TENANT_ID = os.getenv('AZURE_TENANT_ID')
AZURE_CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
AZURE_CLIENT_SECRET = os.getenv('AZURE_CLIENT_SECRET')
AZURE_SUBSCRIPTION_ID = os.getenv('AZURE_SUBSCRIPTION_ID')
AZURE_RESOURCE_GROUP_NAME = os.getenv('AZURE_RESOURCE_GROUP_NAME')
AZURE_STORAGE_ACCOUNT_NAME = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')

def test_storage_table_operations():
    """Test Storage Tables operations"""
    # Create identity with credentials
    identity = Identity(
        tenant_id=AZURE_TENANT_ID,
        client_id=AZURE_CLIENT_ID,
        client_secret=AZURE_CLIENT_SECRET
    )
    
    # Get subscription
    subscription = identity.get_subscription(AZURE_SUBSCRIPTION_ID)
    assert subscription is not None
    print(f"Got subscription: {subscription.subscription_id}")
    
    # Get resource group
    resource_group = subscription.get_resource_group(AZURE_RESOURCE_GROUP_NAME)
    assert resource_group is not None
    print(f"Got resource group: {resource_group.get_name()}")

    # Get storage account service
    storage_account = resource_group.get_storage_account(AZURE_STORAGE_ACCOUNT_NAME)
    assert storage_account is not None
    print(f"Got storage account: {storage_account.get_name()}")

    # Get tables client
    tables_client = storage_account.get_tables_client()
    assert tables_client is not None
    print(f"Got storage tables client successfully")

    # Create a new table in Table Storage 
    table_name = "TestTable"
    table = tables_client.create_sa_table(table_name)
    assert table is not None
    print(f"Successfully created table with table name: {table_name}")

    # Retrieve all the tables in Table Storage 
    table_names = tables_client.get_sa_tables()
    # Verify we got a list of table names
    assert len(table_names) > 0 
    print(f"Successfully retrieved the list of available tables. Table Names: {table_names}")

    # Delete the sa table
    table_deletion_status = tables_client.delete_sa_table(table_name)
    assert table_deletion_status == f"The table {table_name} successfully deleted."
    print(f"The table {table_name} successfully deleted.")

    print("✅ Test passed successfully!")

if __name__ == "__main__":
    pytest.main(["-v", __file__])




