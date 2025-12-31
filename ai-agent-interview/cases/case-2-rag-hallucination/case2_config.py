# Azure-AI related env keys
# NOTE: Request API keys from the interviewer or use your own

OPENAI_API_TYPE = "azure"
OPENAI_API_VERSION = "2025-04-01-preview"

# Azure OpenAI setup
OPENAI_API_BASE = "https://ai-assisstance-openai2.openai.azure.com/"
OPENAI_API_KEY = "YOUR_AZURE_OPENAI_API_KEY_HERE"  # Request from interviewer

# RAG Configuration
# Azure OpenAI for RAG
RAG_OPENAI_API_BASE = OPENAI_API_BASE
RAG_OPENAI_API_KEY = OPENAI_API_KEY
RAG_OPENAI_API_VERSION = OPENAI_API_VERSION
RAG_OPENAI_DEPLOYMENT_ID = "gpt-4o-mini"  # Or use your preferred model

# Azure AI Search for RAG
RAG_AZURE_AI_SEARCH_ENDPOINT = "https://regulation-rag.search.windows.net"
RAG_AZURE_AI_SEARCH_KEY = "YOUR_AZURE_SEARCH_KEY_HERE"  # Request from interviewer
JUSTINE_RAG_AZURE_AI_SEARCH_INDEX_NAME = "justine-rag-index"
SOLA_RAG_AZURE_STORAGE_CONTAINER_NAME = "sola-rag-storage"

# Azure Document Intelligence for RAG
RAG_DOCUMENT_INTELLIGENCE_ENDPOINT = "https://scanpdfocr.cognitiveservices.azure.com/"
RAG_DOCUMENT_INTELLIGENCE_KEY = "YOUR_DOCUMENT_INTELLIGENCE_KEY_HERE"  # Request from interviewer
RAG_DOCUMENT_INTELLIGENCE_MODEL = "prebuilt-invoice"  # prebuilt-invoice or prebuilt-layout
