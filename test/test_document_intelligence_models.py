import sys
import os
import pytest

# Add parent directory to path to import AzWrap
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from AzWrap.wrapper import Identity

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

AZURE_TENANT_ID = os.getenv('AZURE_TENANT_ID')
AZURE_CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
AZURE_CLIENT_SECRET = os.getenv('AZURE_CLIENT_SECRET')
AZURE_SUBSCRIPTION_ID = os.getenv('AZURE_SUBSCRIPTION_ID')
AZURE_RESOURCE_GROUP_NAME = os.getenv('AZURE_RESOURCE_GROUP_NAME')
AZURE_DOCUMENT_INTELLIGENCE_NAME = os.getenv('DOCUMENT_INTELLIGENCE_SERVICE_NAME')

def test_real_document_intelligence_model_administrator():
    """Test actual document intelligence analysis using a real Azure service."""
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
    
    # Get document intelligence service
    doc_service = resource_group.get_document_intelligence_service(AZURE_DOCUMENT_INTELLIGENCE_NAME)
    assert doc_service is not None
    print(f"Got doc service: {doc_service.get_name()}")
    print(f"Service endpoint: {doc_service.get_endpoint()}")
    
    # Get Document Analysis client (using Form Recognizer API)
    fr_client = doc_service.get_formrecognizer_models_client()
    assert fr_client is not None
    print("Got Document Model Administrator client successfully")
    
    # Get a list of all available models
    model_ids = fr_client.get_document_models()
    assert model_ids is not None
    print(f"Got all available Document Intelligence models: {len(model_ids)}")

    # Get the details of a model
    model_details = fr_client.get_document_model_details(model_id=model_ids[0])
    assert model_details is not None
    print(f"Got succesfully the document intelligence model details for the first model")

    # Get Document Analysis client (using Document Intelligence API)
    di_client = doc_service.get_document_intelligence_models_client()
    assert di_client is not None
    print("Got Document Model Administrator client successfully")
    
    # Get a list of all available models
    model_ids = di_client.get_document_models()
    assert model_ids is not None
    print(f"Got all available Document Intelligence models: {len(model_ids)}")

    # Get the details of a model
    model_details = di_client.get_document_model_details(model_id=model_ids[0])
    assert model_details is not None
    print(f"Got succesfully the document intelligence model details for the first model")
    
    print("✅ Test passed successfully!")

if __name__ == "__main__":
    pytest.main(["-v", __file__])