# AzWrap Generalized Hierarchical Indexing Classes

## Overview

Two additional Classes are now added in the `wrapper.py` file, to support the execution of pipelines regarding the knowledge base creation via the generalized hierarchical indexing.

### GenDocParsing

The `GenDocParsing` class is designed to handle the parsing of content from ".docx" files, in the form of objects from the `python-docx` package, by detecting different document sections, with sections being identified in the ".docx" file Headers.

**Purpose**:
- Extracts text content from `Document` files, including paragraphs and tables.
- Handles single-section and multi-section document structures.
- Performs token-based chunking of contents
- Uses OpenAI LLM call to summarize a section's chunks.
- Supports section-based content organization.

**Attributes**:
- `openai_client`: OpenAIClient instance
- `model_name`: LLM name

**Key Methods**:
- `process_document_with_summaries()`: Converts the original document into a dictionary of dictionaries, utilizing all functions of the class. Each key of the dictionary comprises the section name and the values include chunks and a total summary of the section chunks.
- `extract_data()`: Extracts content from the document, handling single or multi-section documents.
- `chunk_section_content(section_content: str, chunk_size: int, overlap: int)`: Performs splitting of section content into chunks with `chunk_size` number of tokens, with `overlap` context tokens.
- `iterate_block_items_with_section()`: Function to iterate through the document's blocks.
- `extract_header_info()`: Extracts the section title from a section header.
- `generate_section_summary(section_title: str, chunks: List[str], max_length: int)`:
Utilizes an LLM call to parse section chunks into a structured Dictionary format. Returns the dictionary or `None` on failure.

**Usage Example**:
```python
openai_client = ai_service.get_OpenAIClient(api_version='2024-05-01-preview')

# Load a .docx file from container (instance of class Container)
doc_instance = container.get_blob_content(file_path)

# Initialize the DocParsing class
doc_parser = GenDocParsing(
    openai_client=openai_client,
    model_name="gpt-4o-mini",
)

# Extract document data and convert to JSON
parsed_data = doc_parser.process_document_with_summaries(doc_instance, file_path)
print(parsed_data)
```

### MultiSectionHandler

The `MultiSectionHandler` class is designed to facilitate the processing of multiple documents and their upload to Azure Search Indexes. Supports both section and chunk indexing.

**Attributes**:
- dict_list: Dictionary extracted from document `process_document_with_summaries()` function of `GenDocParsing` class
- file_name: The full file name, including container subdirectory
- domain: Document domain, uses the container folder in which the document is stored
- index_client_core: Instance of SearchIndex class for Chunk Gen Index
- index_client_detail: Instance of SearchIndex class for Core Gen Index
- openai_client: Instance of OpenAIClient class

**Purpose**:
- Processes multiple documents and prepares them for upload to Index.
- Generates unique IDs for sections and chunks using hashing.
- Creates embeddings for text fields using OpenAI embedding model.
- Supports both section and chunk indexing pipelines.

**Key Methods**:
- `prepare_records_from_processed_sections()`: Processes multiple documents and returns a list of processed records for each document.
- `upload_to_azure_index()`: Uploads processed records to Azure Search indexes, generating embeddings for text fields.
- `prepare_for_upload()`: Prepares all records for upload by coordinating the generation of section IDs and the preparation of both section and chunk records.

**Usage Example**:
```python
# Utilizing instance of GenDocParsing class
parsed_data = doc_parser.process_document_with_summaries(doc_instance, file_path)

# Initialize the MultiSectionHandler
handler = MultiSectionHandler(
    dict_list=parsed_data,
    file_name=file_path,
    domain=container_folder,
    index_client_core_gen=core_gen_index,
    index_client_chunk_gen=chunk_gen_index,
    openai_client=openai_client
)

# Process documents and upload to Azure Search
all_records = handler.prepare_records_from_processed_sections()
handler.upload_to_azure_index(all_records, "core-gen-index-name", "chunk-gen-index-name")
```
