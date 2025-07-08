import sys
import os
import pytest

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
AZURE_DOCUMENT_INTELLIGENCE_NAME = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_NAME')


# Sample document URL for testing - using a simpler, more reliable URL
SAMPLE_DOCUMENT_URL = "https://github.com/Azure-Samples/cognitive-services-REST-api-samples/raw/master/curl/form-recognizer/sample-invoice.pdf"

def test_real_document_intelligence_analyze_from_url():
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
    client = doc_service.get_document_analysis_client()
    assert client is not None
    print("Got Document Analysis client wrapper successfully")
    
    # Analyze document from URL using prebuilt-layout model
    print(f"Analyzing document from URL: {SAMPLE_DOCUMENT_URL}")
    result = client.analyze_document_from_url("prebuilt-layout", SAMPLE_DOCUMENT_URL)
    
    # Verify we got a result
    assert result is not None
    assert "content" in result
    print(f"Successfully analyzed document. Content length: {len(result['content'])}")
    
    if "pages" in result and len(result["pages"]) > 0:
        print(f"Number of pages: {len(result['pages'])}")
        first_page = result["pages"][0]
        if "page_number" in first_page:
            assert first_page["page_number"] == 1
            print(f"First page number: {first_page['page_number']}")


    # Get Document Intelligence client (using Document Intelligence API)
    di_client = doc_service.get_document_intelligence_client()
    assert di_client is not None
    print("Got Document Analysis client wrapper successfully")
    
    # Analyze document from URL using prebuilt-layout model
    print(f"Analyzing document from URL: {SAMPLE_DOCUMENT_URL}")
    result = di_client.analyze_document_from_url("prebuilt-layout", SAMPLE_DOCUMENT_URL)
    
    # Verify we got a result
    assert result is not None
    assert "content" in result
    print(f"Successfully analyzed document. Content length: {len(result['content'])}")
    
    if "pages" in result and len(result["pages"]) > 0:
        print(f"Number of pages: {len(result['pages'])}")
        first_page = result["pages"][0]
        if "page_number" in first_page:
            assert first_page["page_number"] == 1
            print(f"First page number: {first_page['page_number']}")


    
    print("✅ Test passed successfully!")

if __name__ == "__main__":
    pytest.main(["-v", __file__])