# AzWrap Document Intelligence Integration

This document describes the Document Intelligence capability in the AzWrap library, which provides a streamlined wrapper for Azure Form Recognizer services.

## Overview

Azure Document Intelligence (formerly Form Recognizer) is an AI service that applies machine learning to extract text, key-value pairs, tables, and structure from documents. The AzWrap integration uses both the Azure Form Recognizer SDK (`azure-ai-formrecognizer`) and Document Intelligence SDK (`azure-ai-documentintelligence`), following the same hierarchical approach used for other Azure services in the library:

For Azure Form Recognizer SDK
- Identity → Subscription → ResourceGroup → DocumentIntelligenceService → DocumentAnalysisClientWrapper OR FormRecognizerModels

For Document Intelligence SDK
- Identity → Subscription → ResourceGroup → DocumentIntelligenceService → DocumentIntelligenceClientWrapper OR DocumentIntelligenceModels

**Note**: This implementation uses the Azure Form Recognizer SDK which supports both legacy Form Recognizer services and newer Document Intelligence services deployed with the "FormRecognizer" kind.

## Installation

The Document Intelligence integration requires the `azure-ai-formrecognizer` and `azure-ai-documentintelligence` packages:

```bash
pip install azure-ai-formrecognizer>=3.3.0 
pip install azure-ai-documentintelligence==1.0.2
```

This dependencies are automatically included when installing AzWrap:

```bash
pip install azwrap
```

## Requirements

- Azure subscription with a Form Recognizer or Document Intelligence service
- Service must be deployed with kind "FormRecognizer" or "DocumentIntelligence"
- Valid Azure credentials (tenant ID, client ID, client secret)

## Usage

### Getting a Document Intelligence Service

```python
from azwrap import Identity, Subscription, ResourceGroup, DocumentIntelligenceService

# Create an identity with your Azure credentials
identity = Identity(tenant_id, client_id, client_secret)

# Get a subscription
subscription = identity.get_subscription(subscription_id)

# Get a resource group
resource_group = subscription.get_resource_group(group_name)

# Get a Document Intelligence service
doc_intelligence = resource_group.get_document_intelligence_service(service_name)
```

### Working with Document Intellignece Models Administrator Client

```python
# Get a client for managing document models
models_client = doc_intelligence.get_document_intelligence_models_client()

# List all document model IDs in the current Document Intelligence resource
model_ids = models_client.get_document_models()

# Retrieve metadata and details about a specific model by its ID
details = models_client.get_document_model_details("model-id")

# Create and train a custom document model using training data in an Azure Blob Storage container.
model = models_client.create_document_model(
    model_id="my-model",
    build_mode="template",
    blob_container_url="https://<account>.blob.core.windows.net/<container>",
    folder_path="invoices/training",
    description="Invoice processing model"
)

# Copy custom document model to another document intelligence resource.
copied_model_details = models_client.copy_document_model(model_id="my-model", target_endpoint=target_endpoint, target_key=target_key)

# Delete a specific custom document model from the Azure resource.
models_client.delete_model("my-model")
```

### Working with Form Recognizer Models Administrator Client

```python
# Get a client for managing document models
models_client = doc_intelligence.get_formrecognizer_models_client()

# List all document model IDs in the current Document Intelligence resource
model_ids = models_client.get_document_models()

# Retrieve metadata and details about a specific model by its ID
details = models_client.get_document_model_details("model-id")

# Create and train a custom document model using training data in an Azure Blob Storage container.
model = models_client.create_document_model(
    model_id="my-model",
    build_mode="template",
    blob_container_url="https://<account>.blob.core.windows.net/<container>",
    folder_path="invoices/training",
    description="Invoice processing model"
)

# Copy custom document model to another document intelligence resource.
copied_model_details = models_client.copy_document_model(model_id="my-model", target_endpoint=target_endpoint, target_key=target_key)

# Delete a specific custom document model from the Azure resource.
models_client.delete_model("my-model")
```

### Working with Document Intelligence Client 

```python
# Get a Document Analysis client (uses Form Recognizer SDK)
client = doc_intelligence.get_document_intelligence_client()

# Analyze a document using a specific model
result = client.analyze_document("prebuilt-layout", "/path/to/document.pdf")

# Analyze a document from a URL
result = client.analyze_document_from_url("prebuilt-layout", "https://example.com/document.pdf")

# Analyze a document using a custom model 
result = client.analyze_custom_document("your-custom-model", "/path/to/document.pdf")

# Analyze a document from a URL using a custom model
result = client.analyze_custom_document_from_url("your-custom-model", "https://example.com/document.pdf")
```


### Working with Document Analysis Client (With Form Recognizer API)

```python
# Get a Document Analysis client (uses Form Recognizer SDK)
client = doc_intelligence.get_document_analysis_client()

# Analyze a document using a specific model
result = client.analyze_document("prebuilt-layout", "/path/to/document.pdf")

# Analyze a document from a URL
result = client.analyze_document_from_url("prebuilt-layout", "https://example.com/document.pdf")

# Analyze a document using a custom model 
result = client.analyze_custom_document("your-custom-model", "/path/to/document.pdf")

# Analyze a document from a URL using a custom model
result = client.analyze_custom_document_from_url("your-custom-model", "https://example.com/document.pdf")
```

### Supported Models

The following prebuilt models are available:
- `prebuilt-layout` - Extract text, tables, and structure
- `prebuilt-receipt` - Extract receipt information
- `prebuilt-invoice` - Extract invoice information  
- `prebuilt-idDocument` - Extract ID document information
- `prebuilt-businessCard` - Extract business card information
- `prebuilt-tax.us.w2` - Extract W-2 tax form information
- `prebuilt-tax.us.1098` - Extract 1098 tax form information
- `prebuilt-tax.us.1099` - Extract 1099 tax form information
- `prebuilt-healthInsuranceCard.us` - Extract health insurance card information

### Convenience Methods for Document Types

The client provides specialized methods for different document types:

#### Basic Document Types
```python
# Analyze document layout
layout_result = client.analyze_layout("/path/to/document.pdf")

# Analyze receipts
receipt_result = client.analyze_receipt("/path/to/receipt.jpg")

# Analyze invoices
invoice_result = client.analyze_invoice("/path/to/invoice.pdf")

# Analyze ID documents
id_result = client.analyze_id_document("/path/to/passport.jpg")

# Analyze business cards
card_result = client.analyze_business_card("/path/to/card.jpg")
```

#### Tax Forms
```python
# Analyze W-2 forms
w2_result = client.analyze_w2("/path/to/w2.pdf")

# Analyze 1098 forms
form_1098_result = client.analyze_1098("/path/to/1098.pdf")

# Analyze 1099 forms
form_1099_result = client.analyze_1099("/path/to/1099.pdf")
```

#### Specialized Documents
```python
# Analyze health insurance cards
insurance_result = client.analyze_health_insurance_card("/path/to/insurance_card.jpg")
```

**Note**: Other specialized document types and custom models are supported by passing the appropriate model ID to the `analyze_document()` or `analyze_document_from_url()` methods.

## DocumentIntelligenceService Class

The `DocumentIntelligenceService` class provides access to a Document Intelligence service in Azure.

### Properties

- `name`: The name of the service
- `location`: The Azure region where the service is deployed
- `endpoint`: The service endpoint URL
- `kind`: The type of service (FormRecognizer or DocumentIntelligence)
- `sku`: The SKU tier of the service
- `id`: The Azure resource ID

### Methods

- `get_name()`: Returns the service name
- `get_id()`: Returns the Azure resource ID
- `get_location()`: Returns the Azure region
- `get_kind()`: Returns the service kind
- `get_sku()`: Returns the SKU name
- `get_endpoint()`: Returns the service endpoint URL
- `get_keys()`: Returns a dictionary with primary and secondary keys
- `get_credential()`: Returns an `AzureKeyCredential` for authentication
- `get_document_analysis_client()`: Returns a client for document analysis
- `get_document_models_client()`: Returns a client for document model management


## DocumentIntelligenceModels Class

The `DocumentIntelligenceModels` class provides an interface for managing custom document models in the Azure Document Intelligence service. It wraps the Azure SDK's `DocumentModelAdministrationClient` and is accessible from the `DocumentIntelligenceService` class.

### Properties

- `document_intelligence_service`: Reference to the parent `DocumentIntelligenceService` instance
- `client`: The underlying `DocumentModelAdministrationClient` used for model operations

### Methods

- `get_document_models()`: Returns a list of all custom model IDs in the Azure resource
- `get_document_model_details()`: Retrieves detailed metadata for a specified model
- `create_document_model()`: Creates and trains a new custom model from labeled documents in Azure Blob Storage
- `delete_model()`: Deletes a custom model by its ID
- `copy_document_model()`: Copies a custom model to a target resource


## DocumentIntelligenceClientWrapper Class

The `DocumentIntelligenceClientWrapper` wraps the Azure SDK's `DocumentAnalysisClient` from the Form Recognizer package to provide a more convenient interface.

### General Methods

- `get_service()`: Returns the parent DocumentIntelligenceService
- `get_client()`: Returns the underlying Azure SDK client
- `analyze_document()`: Analyzes a document using a specified model
- `analyze_document_from_url()`: Analyzes a document from a URL

### Document-Specific Methods

- `analyze_layout()`: Extracts text, tables, and selection marks
- `analyze_layout_from_url()`: Same as above but from a URL (calls analyze_document_from_url with "prebuilt-layout")
- `analyze_receipt()`: Extracts information from receipts
- `analyze_invoice()`: Extracts information from invoices
- `analyze_id_document()`: Extracts information from ID documents
- `analyze_business_card()`: Extracts information from business cards

## Results Format

Analysis results are returned as dictionaries with the following structure:

```python
{
    "content": "Full document text content",
    "pages": [
        {
            "page_number": 1,
            "lines": [
                {
                    "content": "Line of text",
                    "bounding_box": [coordinates]
                },
                # More lines...
            ],
            "tables": [
                {
                    "row_count": 3,
                    "column_count": 4,
                    "cells": [
                        {
                            "row_index": 0,
                            "column_index": 0,
                            "content": "Cell content",
                            "kind": "content"
                        },
                        # More cells...
                    ]
                },
                # More tables...
            ]
        },
        # More pages...
    ]
}
```

For documents with key-value pairs (like receipts, invoices), the result will also include:

```python
{
    # ... other fields
    "key_value_pairs": [
        {
            "key": "Date",
            "value": "2023-04-15"
        },
        {
            "key": "Total",
            "value": "$42.99"
        },
        # More key-value pairs...
    ]
}
```

## CLI Usage

The AzWrap CLI provides comprehensive Document Intelligence commands:

### Service Management
```bash
# List all Document Intelligence services
azwrap document list

# List services in a specific resource group
azwrap document list --resource-group my-resource-group

# Get details of a specific service
azwrap document get --name my-doc-service --resource-group my-resource-group
```

### Document Analysis
```bash
# Analyze with any model (local file)
azwrap document analyze --service-name my-doc-service --resource-group my-rg --model prebuilt-layout --document-path /path/to/document.pdf

# Analyze with any model (URL)
azwrap document analyze --service-name my-doc-service --resource-group my-rg --model prebuilt-invoice --document-url https://example.com/invoice.pdf

# Save results to file
azwrap document analyze --service-name my-doc-service --resource-group my-rg --model prebuilt-receipt --document-path receipt.jpg --output-file results.json
```

### Specialized Analysis Commands
```bash
# Layout analysis
azwrap document analyze-layout --service-name my-doc-service --resource-group my-rg --document-path document.pdf

# Receipt analysis
azwrap document analyze-receipt --service-name my-doc-service --resource-group my-rg --document-path receipt.jpg

# Invoice analysis
azwrap document analyze-invoice --service-name my-doc-service --resource-group my-rg --document-path invoice.pdf

# ID document analysis
azwrap document analyze-id --service-name my-doc-service --resource-group my-rg --document-path passport.jpg

# Business card analysis
azwrap document analyze-business-card --service-name my-doc-service --resource-group my-rg --document-path card.jpg

# W-2 tax form analysis
azwrap document analyze-w2 --service-name my-doc-service --resource-group my-rg --document-path w2.pdf
```

### Custom Model Analysis
```bash
# Analyze with custom model
azwrap document analyze-custom --service-name my-doc-service --resource-group my-rg --model-id my-custom-model --document-path custom-doc.pdf
```

### Batch Processing
```bash
# Analyze folder of documents
azwrap document analyze-batch --service-name my-doc-service --resource-group my-rg --model prebuilt-layout --document-folder /path/to/documents --output-folder /path/to/results

# Analyze from document list file
azwrap document analyze-batch --service-name my-doc-service --resource-group my-rg --model prebuilt-receipt --document-list document_list.txt --output-folder /path/to/results
```

### Output Formats
```bash
# JSON output
azwrap --output json document analyze-layout --service-name my-doc-service --resource-group my-rg --document-path document.pdf

# Table output
azwrap --output table document list
```

## Error Handling

All client methods use the `@retry` decorator to automatically retry on transient failures, with exponential backoff. Exceptions are propagated to the caller after the retry attempts are exhausted.

### Common Issues

#### ImportError: No module named 'azure.ai.formrecognizer'
**Solution**: Install the Form Recognizer package:
```bash
pip install azure-ai-formrecognizer>=3.3.0
```

#### 404 Resource Not Found
**Possible causes**:
- Service name is incorrect
- Service is not of kind "FormRecognizer" or "DocumentIntelligence"
- Model ID is not supported (check supported models list above)
- Service endpoint is incorrect

**Solution**: Verify service exists and check the service kind:
```python
# Check if service exists and get its properties
doc_service = resource_group.get_document_intelligence_service("your-service-name")
if doc_service:
    print(f"Service kind: {doc_service.get_kind()}")
    print(f"Service endpoint: {doc_service.get_endpoint()}")
else:
    print("Service not found")
```

#### Authentication Errors
**Solution**: Ensure your Azure credentials have the necessary permissions:
- Cognitive Services User role
- Access to the resource group containing the service

### Supported Service Kinds

The integration works with Azure services that have one of these kinds:
- `FormRecognizer` (legacy Form Recognizer services)
- `DocumentIntelligence` (newer Document Intelligence services)

Both kinds are supported by the Form Recognizer SDK used in this implementation.