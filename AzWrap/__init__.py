# AzWrap package
"""
Azure Wrapper Library - Simplifies interaction with Azure services
"""

# Version
__version__ = "0.1.7"

# Identity and Resource Management
from .wrapper import (
    ResourceNotFoundError,
    Identity,
    Subscription,
    ResourceGroup,
    
    # Storage
    StorageAccount,
    Container,
    Table,
    BlobType,
    
    # Search
    SearchService, 
    SearchIndex,
    SearchIndexerManager,
    DataSourceConnection,
    Indexer,
    Skillset,
    get_std_vector_search,
    
    # AI Services
    AIService,
    OpenAIClient,
    
    # Document Intelligence
    DocumentIntelligenceService,
    DocumentIntelligenceClientWrapper,
    DocumentIntelligenceModels,
    DocumentAnalysisClientWrapper,
    FormRecognizerModels
)

# CLI functionality
from .main import main as cli_main

# Convenient access to common classes and functions
__all__ = [
    "ResourceNotFoundError",
    # Identity and Resource Management
    "Identity",
    "Subscription", 
    "ResourceGroup",
    
    # Storage
    "StorageAccount",
    "Container",
    "Table",
    "BlobType",
    
    # Search Services
    "SearchService",
    "SearchIndex",
    "SearchIndexerManager",
    "DataSourceConnection",
    "Indexer",
    "Skillset",
    "get_std_vector_search",
    
    # AI Services
    "AIService",
    "OpenAIClient",
    
    # Document Intelligence
    "DocumentIntelligenceService",
    "DocumentIntelligenceClientWrapper",
    "DocumentIntelligenceModels",
    "DocumentAnalysisClientWrapper",
    "FormRecognizerModels",
    
    # CLI
    "cli_main"
]
