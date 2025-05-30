# AzWrap Hierarchical Indexing Classes

## Overview

Two additional Classes are now added in the `wrapper.py` file, to support the execution of pipelines regarding the knowledge base creation via hierarchical indexing.

### DocParsing

The `DocParsing` class is designed to handle the parsing of content from ".docx" files, in the form of objects from the `python-docx` package.

**Purpose**:
- Extracts text content from `Document` files, including paragraphs and tables.
- Handles single-process and multi-process document structures.
- Uses OpenAI LLM call to parse and structure content into JSON format.
- Supports metadata extraction and section-based content organization.

**Attributes**:
- `openai_client`: OpenAIClient instance
- `json_format`: Format of JSON to be produced from document
- `domain`: Document domain
- `model_name`: LLM name

**Key Methods**:
- `doc_to_json()`: Converts an original document, in python-docx "Document" format, into a list of dictionaries (JSON string), utilizing all functions of the class. Fields of the dictionary include multiple metadata for the document.
- `extract_data()`: Extracts content from the document, handling single or multi-process structures.
- `_is_single_process()`: Determines whether the document contains a single process or multiple processes based on headers.
- `_iterate_block_items_with_section()`: Function to iterate through the document's blocks.
- `_extract_header_info()`: Extracts the process title from a section header.
- `update_json_with_ai(content_to_parse: str, process_identifier: str, doc_name: str)`:
Utilizes an LLM call to parse document content into a structured JSON format. Returns the JSON string or `None` on failure.

**Usage Example**:
```python
openai_client = ai_service.get_OpenAIClient(api_version='2024-05-01-preview')

# Load a .docx file from container (instance of class Container)
doc_instance = container.get_blob_content(file_path)

# Define a JSON format template
json_format = {
    "process_name": "",
    "related_processes": [],
    "short_description": "",
    "introduction": "",
    "reference_documents": [],
    "forms_documents" : [],
    "systems_manuals_used" : [],
    "related_products": [],
    "additional_information":"",
    "steps": [
        {
            "step_number": "",
            "step_name": "",
            "step_description": "",
            "systems_used": [],
            "documents_used": []
        }
    ]
}

# Initialize the DocParsing class
doc_parser = DocParsing(
    openai_client=openai_client,
    json_format=json_format,
    domain="Finance",
    model_name="gpt-4o-mini",
)

# Extract document data and convert to JSON
parsed_data = doc_parser.doc_to_json(doc_instance, file_path, container_folder)
print(parsed_data)
```

### MultiProcessHandler

The `MultiProcessHandler` class is designed to facilitate the processing of multiple documents and their upload to Azure Search Indexes. Supports both process and step indexing.

**Attributes**:
- dict_list: JSON extracted from document `doc_to_json()` function of `DocParsing` class
- index_client_core: Instance of SearchIndex class for Detail Index
- index_client_detail: Instance of SearchIndex class for Core Index
- openai_client: Instance of OpenAIClient class

**Purpose**:
- Processes multiple documents and prepares them for upload to Index.
- Generates unique IDs for processes and steps using hashing.
- Creates embeddings for text fields using OpenAI embedding model.
- Supports both core and detailed indexing pipelines.

**Key Methods**:
- `process_documents()`: Processes multiple documents and returns a list of processed records for each document.
- `upload_to_azure_index()`: Uploads processed records to Azure Search indexes, generating embeddings for text fields.
- `prepare_for_upload()`: Prepares all records for upload by coordinating the generation of process IDs and the preparation of both core and detailed records.

**Usage Example**:
```python
# Utilizing instance of DocParsing class
parsed_data = doc_parser.doc_to_json(doc_instance, file_path, container_folder)

# Initialize the MultiProcessHandler
handler = MultiProcessHandler(
    dict_list=parsed_data,
    core_index=core_index,
    core_index=detail_index,
    openai_client=openai_client
)

# Process documents and upload to Azure Search
all_records = handler.process_documents()
handler.upload_to_azure_index(all_records, "core-index-name", "detailed-index-name")
```
