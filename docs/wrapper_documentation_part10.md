# AzWrap Table Storage Integration

The `Table` class provides access to Azure Table Storage resources through a connected `StorageAccount` class. It enables listing, creating, deleting tables, and performing entity-level operations (insert, delete, retrieve) using data from CSV files.

### Hierarchy

`Identity → Subscription → ResourceGroup → StorageAccount → Table`

### Requirements

- Azure Storage Account with Table service enabled
- `azure-data-tables` Python package
- CSV files encoded in UTF-8, using a pipe (|) delimiter, with no headers and fields structured according to the expected table schema.


## Installation

The Table Storage integration requires the `azure-data-tables ` package:

```bash
pip install azure-data-tables==12.7.0
```

This dependency is automatically included when installing AzWrap:

```bash
pip install azwrap
```

## Usage

### Getting a Table Storage Service

```python
from azwrap import Identity, Subscription, ResourceGroup, StorageAccount, Table

# Create an identity with your Azure credentials
identity = Identity(tenant_id, client_id, client_secret)

# Get a subscription
subscription = identity.get_subscription(subscription_id)

# Get a resource group
resource_group = subscription.get_resource_group(group_name)

# Get a Document Intelligence service
doc_intelligence = resource_group.get_document_intelligence_service(service_name)

# Get Storage Account service
storage_account = resource_group.get_storage_account(strogage_account_name)

# Get Storage Tables client
tables_client = storage_account.get_tables_client()
```

### Working with Table Client

```python
# Retrieve all the tables in table storage 
table_names = tables_client.get_sa_tables()

# Create a new table in table storage 
table = tables_client.create_sa_table(table_name)

# Upload data to a table from csv or txt file
upload_status = tables_client.upload_entities_from_csv(source_csv, table_name, table_schema)

# Get all the entries from the table
entities_df = tables_client.get_entities(table_name)

# Delete the table entities from csv or txt file
deletion_status = tables_client.delete_entities_from_csv(source_csv, table_name, table_schema)

# Delete the sa table
table_deletion_status =tables_client.delete_sa_table(table_name)
```

## Table Class

The `Table` class provides access to a Table Storage service in Azure.


## Properties

- `storage_account`: The associated `StorageAccount` instance
- `connection_string`: The storage account's connection string
- `table_service_client`: Instance of `TableServiceClient` to manage table-level operations

### Methods

- `get_sa_tables()`: Returns a list of table names in the storage account.
- `create_sa_table(table_name)`: Creates a new table or returns the existing one as a `TableClient`.
- `delete_sa_table(table_name)`: Deletes the specified table and returns a confirmation message.
- `upload_entities_from_csv(csv_path, table_name, table_schema, delimeter='|')`: Uploads entities from a CSV file shaped with the provided schema; replaces any existing ones.
- `delete_entities_from_csv(csv_path, table_name, table_schema, delimeter='|')`: Deletes entities from a table using keys from a CSV file.
- `get_entities(table_name)`: Returns all entities from a table as a pandas `DataFrame`.

