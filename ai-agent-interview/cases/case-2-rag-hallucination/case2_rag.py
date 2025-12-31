"""
Case2 SDK - Base Carbone Factors Indexing using LangChain
Indexes Base Carbone emission factors from Base_Carbone_V23.6.xlsx to Azure AI Search
Uses LangChain with Azure OpenAI and Azure AI Search for RAG
"""
import os
import re
import logging
from typing import List, Optional, Dict, Any, Tuple
from django.conf import settings
from pathlib import Path
from openpyxl import load_workbook
from datetime import datetime
import json
import time
import pandas as pd
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from langchain.schema import Document
from langchain_community.chat_models import AzureChatOpenAI
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

logger = logging.getLogger(__name__)

# ============================================================
# CONFIGURATION - Azure OpenAI and Azure AI Search
# ============================================================
# Azure OpenAI Configuration
AZURE_OPENAI_API_BASE = getattr(settings, 'RAG_OPENAI_API_BASE', settings.OPENAI_API_BASE)
AZURE_OPENAI_API_KEY = getattr(settings, 'RAG_OPENAI_API_KEY', settings.OPENAI_API_KEY)
AZURE_OPENAI_API_VERSION = getattr(settings, 'RAG_OPENAI_API_VERSION', settings.OPENAI_API_VERSION)
AZURE_OPENAI_DEPLOYMENT_ID = getattr(settings, 'RAG_OPENAI_DEPLOYMENT_ID', 'gpt-4o-mini')

# Azure AI Search Configuration
AZURE_SEARCH_ENDPOINT = getattr(settings, 'RAG_AZURE_AI_SEARCH_ENDPOINT', '')
AZURE_SEARCH_KEY = getattr(settings, 'RAG_AZURE_AI_SEARCH_KEY', '')

# Embedding Configuration
EMBEDDING_DEPLOYMENT_ID = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 256

# Index names
# Schema matches Base Carbone factors from Base_Carbone_V23.6.xlsx
SOLA_RAG_INDEX_NAME = getattr(settings, 'SOLA_RAG_AZURE_AI_SEARCH_INDEX_NAME', 'sola-rag-index')

# ============================================================
# LANGCHAIN SETUP
# ============================================================

# Custom embedding function that ensures dimensions=256
def create_embedding_with_dimensions(text: str) -> List[float]:
    """
    Create embedding with explicit dimensions=256 parameter.
    This ensures compatibility with Azure AI Search index that expects 256 dimensions.
    """
    from openai import AzureOpenAI
    azure_client = AzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
        azure_endpoint=AZURE_OPENAI_API_BASE.rstrip("/"),
    )
    response = azure_client.embeddings.create(
        model=EMBEDDING_DEPLOYMENT_ID,
        input=[text],
        dimensions=EMBEDDING_DIMENSIONS,  # CRITICAL: Specify 256 dimensions
    )
    return response.data[0].embedding

# Initialize LangChain LLM (lazy initialization to avoid conflicts)
_llm = None

def get_llm():
    """Get or create LangChain AzureChatOpenAI instance"""
    global _llm
    if _llm is None:
        # Temporarily unset OPENAI_API_BASE env var to prevent LangChain from auto-setting base_url
        # This avoids conflict with azure_endpoint parameter (especially on Azure where env vars are set)
        import os
        original_base_url = os.environ.pop("OPENAI_API_BASE", None)
        original_base_url_alt = os.environ.pop("AZURE_OPENAI_API_BASE", None)
        
        try:
            _llm = AzureChatOpenAI(
                azure_deployment=AZURE_OPENAI_DEPLOYMENT_ID,
                openai_api_version=AZURE_OPENAI_API_VERSION,
                azure_endpoint=AZURE_OPENAI_API_BASE.rstrip("/"),
                api_key=AZURE_OPENAI_API_KEY,
                temperature=0.7,
            )
        finally:
            # Restore original env vars if they existed (to avoid side effects)
            if original_base_url is not None:
                os.environ["OPENAI_API_BASE"] = original_base_url
            if original_base_url_alt is not None:
                os.environ["AZURE_OPENAI_API_BASE"] = original_base_url_alt
    return _llm

# Helper function to get vector store
def get_vector_store(rag_type: str = "sola") -> AzureSearch:
    """
    Get LangChain AzureSearch vector store for Sola RAG.
    
    Args:
        rag_type: "sola"
    
    Returns:
        AzureSearch vector store instance
    """
    index_name = SOLA_RAG_INDEX_NAME
    
    return AzureSearch(
        azure_search_endpoint=AZURE_SEARCH_ENDPOINT,
        azure_search_key=AZURE_SEARCH_KEY,
        index_name=index_name,
        embedding_function=create_embedding_with_dimensions,  # Use custom function with dimensions=256
    )

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def clean_text(value: Optional[Any]) -> Optional[str]:
    """Clean text value, handling None and converting to string"""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return str(value) if not pd.isna(value) else None
    text = str(value).strip()
    return text if text and text.lower() != "nan" else None


def safe_float(value: Optional[Any]) -> Optional[float]:
    """Safely convert value to float"""
    if value is None:
        return None
    try:
        if isinstance(value, str):
            # Handle French number format (comma as decimal separator)
            value = value.replace(",", ".")
        return float(value)
    except (ValueError, TypeError):
        return None


def parse_excel_datetime(value: Optional[Any]) -> Optional[datetime]:
    """Parse Excel datetime value"""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            # Try common date formats
            for fmt in ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"]:
                try:
                    return datetime.strptime(value, fmt)
                except ValueError:
                    continue
        except:
            pass
    return None


def build_base_carbone_content_text(record: Dict[str, Any]) -> str:
    """
    Build searchable content text from Base Carbone factor record.
    Similar to build_search_query in map_invoices_to_base_carbone.py
    """
    parts = []
    
    # Name (French and English)
    if record.get("name_fr"):
        parts.append(f"Nom français: {record['name_fr']}")
    if record.get("name_en"):
        parts.append(f"Nom anglais: {record['name_en']}")
    
    # Category
    if record.get("category"):
        parts.append(f"Catégorie: {record['category']}")
    
    # Tags
    if record.get("tags_fr"):
        parts.append(f"Tags français: {record['tags_fr']}")
    if record.get("tags_en"):
        parts.append(f"Tags anglais: {record['tags_en']}")
    
    # Units
    if record.get("unit_fr"):
        parts.append(f"Unité français: {record['unit_fr']}")
    if record.get("unit_en"):
        parts.append(f"Unité anglais: {record['unit_en']}")
    
    # Location
    if record.get("location"):
        parts.append(f"Localisation: {record['location']}")
    
    # Programme and Source
    if record.get("programme"):
        parts.append(f"Programme: {record['programme']}")
    if record.get("source"):
        parts.append(f"Source: {record['source']}")
    
    # Comments
    if record.get("comments_fr"):
        parts.append(f"Commentaire français: {record['comments_fr']}")
    if record.get("comments_en"):
        parts.append(f"Commentaire anglais: {record['comments_en']}")
    
    # Emission values
    if record.get("total") is not None:
        parts.append(f"Total CO2e: {record['total']}")
    
    return ". ".join(parts) + "."


def sanitize_key(value: str) -> str:
    """
    Sanitize a string to be used as Azure Search document key:
    allow letters, digits, underscore (_), dash (-), equal sign (=).
    Replace other chars with underscore.
    """
    sanitized = re.sub(r"[^A-Za-z0-9_=-]", "_", value)
    return sanitized or "doc"


def clean_for_json(value: Any) -> Any:
    """
    Clean value for JSON serialization:
    - Convert NaN/NaT to None
    - Keep datetime as datetime object (Azure Search SDK will serialize it)
    - Handle pandas NaN values
    - Keep other values as-is
    """
    import math
    
    if value is None:
        return None
    
    # Check for pandas NaN/NaT first (before type checking)
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass  # Not a pandas-compatible type
    
    # Keep datetime as datetime object - Azure Search SDK will handle serialization
    if isinstance(value, datetime):
        return value if value else None
    
    if isinstance(value, float):
        # Check for NaN/Inf using math.isfinite (not pd.isfinite)
        try:
            if pd.isna(value) or not math.isfinite(value):
                return None
        except (TypeError, ValueError):
            return None
        return value
    
    if isinstance(value, int):
        return value
    
    if isinstance(value, str):
        # Remove any NaN string representations
        if value.lower() in ['nan', 'nat', 'none', 'null', '']:
            return None
        return value
    
    # For other types, try to convert to string or return as-is
    return value


# ============================================================
# BASE CARBONE EXCEL PROCESSOR
# ============================================================
class BaseCarboneExcelProcessor:
    """Process Base Carbone Excel file: Parse → Embedding → Indexing to Azure AI Search"""
    
    def upload_base_carbone_excel(
        self,
        excel_file_path: str,
        filename: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Ingest Base_Carbone_V23.6.xlsx and index into Azure AI Search.
        Logic follows map_invoices_to_base_carbone.py but uses Azure AI Search instead of local files.
        
        Args:
            excel_file_path: Path to Base_Carbone_V23.6.xlsx file
            filename: Optional filename (defaults to excel_file_path basename)
        
        Returns:
            Dict with status, file info, and indexing results
        """
        try:
            excel_path = Path(excel_file_path)
            
            # Check for fallback paths (similar to map_invoices_to_base_carbone.py lines 1715-1743)
            if not excel_path.exists():
                    error_msg = f"Base Carbone Excel file not found at {excel_file_path} and no fallback available"
                    print(f"[Base Carbone] ERROR: {error_msg}")
                    logger.error(error_msg)
                    return {
                        "status": "error",
                        "error": error_msg,
                    }
            
            print(f"[Base Carbone] Starting upload for file {excel_path}")
            logger.info(f"Base Carbone: Starting upload for file {excel_path}")
            
            # Load Excel file using pandas
            df = pd.read_excel(excel_path, engine='openpyxl', sheet_name='All_Records')
            
            if df.empty:
                error_msg = f"Excel file is empty or sheet 'All_Records' not found in {excel_path}"
                print(f"[Base Carbone] ERROR: {error_msg}")
                logger.error(error_msg)
                return {
                    "status": "error",
                    "error": error_msg,
                }
            
            print(f"[Base Carbone] Loaded Excel file with {len(df.columns)} columns, {len(df)} rows")
            logger.info(f"Base Carbone: Loaded Excel file with {len(df.columns)} columns, {len(df)} rows")
            
            # Parse rows and build documents
            documents: List[Dict[str, Any]] = []
            count = 0

            
            for idx, row in df.iterrows():
                # Build payload from row (pandas Series to dict)
                # Note: Column names are in original case (not lowercased) for mapping
                payload = row.to_dict()
                print(f"[Base Carbone] Row {idx+1} - Payload keys: {list(payload.keys())[:5]}...")
                
                # Extract fields (matching FactorRecord structure)
                # Handle identifier separately (can be int or NaN)
                identifier_val = payload.get("Identifiant de l'élément")
                if identifier_val is not None:
                    try:
                        if pd.notna(identifier_val):
                            identifier_val = int(float(identifier_val)) if not pd.isna(identifier_val) else None
                        else:
                            identifier_val = None
                    except (ValueError, TypeError):
                        identifier_val = None
                else:
                    identifier_val = None
                
                record = {
                    "row_index": int(idx) + 1,  # 1-based (pandas idx is 0-based), matching Base Carbone logic
                    "identifier": identifier_val,
                    "status": clean_text(payload.get("Statut de l'élément")),
                    "name_fr": clean_text(payload.get("Nom base français")),
                    "name_en": clean_text(payload.get("Nom base anglais")),
                    "category": clean_text(payload.get("Code de la catégorie")),
                    "tags_fr": clean_text(payload.get("Tags français")),
                    "tags_en": clean_text(payload.get("Tags anglais")),
                    "unit_fr": clean_text(payload.get("Unité français")),
                    "unit_en": clean_text(payload.get("Unité anglais")),
                    "contributor": clean_text(payload.get("Contributeur")),
                    "other_contributors": clean_text(payload.get("Autres Contributeurs")),
                    "programme": clean_text(payload.get("Programme")),
                    "source": clean_text(payload.get("Source")),
                    "url": clean_text(payload.get("Url du programme")),
                    "location": clean_text(payload.get("Localisation géographique")),
                    "created_at": parse_excel_datetime(payload.get("Date de création")),
                    "modified_at": parse_excel_datetime(payload.get("Date de modification")),
                    "validity": clean_text(payload.get("Période de validité")),
                    "comments_fr": clean_text(payload.get("Commentaire français")),
                    "comments_en": clean_text(payload.get("Commentaire anglais")),
                    "total": safe_float(payload.get("Total poste non décomposé")),
                    "co2f": safe_float(payload.get("CO2f")),
                    "ch4f": safe_float(payload.get("CH4f")),
                    "ch4b": safe_float(payload.get("CH4b")),
                    "n2o": safe_float(payload.get("N2O")),
                    "extra_gases": json.dumps([
                        {
                            "code": clean_text(payload.get("Code gaz supplémentaire 1")),
                            "value": safe_float(payload.get("Valeur gaz supplémentaire 1")),
                        },
                        {
                            "code": clean_text(payload.get("Code gaz supplémentaire 2")),
                            "value": safe_float(payload.get("Valeur gaz supplémentaire 2")),
                        },
                        {
                            "code": clean_text(payload.get("Code gaz supplémentaire 3")),
                            "value": safe_float(payload.get("Valeur gaz supplémentaire 3")),
                        },
                        {
                            "code": clean_text(payload.get("Code gaz supplémentaire 4")),
                            "value": safe_float(payload.get("Valeur gaz supplémentaire 4")),
                        },
                        {
                            "code": clean_text(payload.get("Code gaz supplémentaire 5")),
                            "value": safe_float(payload.get("Valeur gaz supplémentaire 5")),
                        },
                    ]),
                }

                # print(f"[Base Carbone] Record: {record}") 
                # logger.info(f"Base Carbone: Record: {record}")
                # Build content text for search
                content_text = build_base_carbone_content_text(record)
                
                # Build document for indexing
                # Keep datetime objects (don't convert to ISO string) - Azure Search SDK will handle serialization
                doc = {
                    "content": content_text,
                    "row_index": record["row_index"],
                    "identifier": record["identifier"],
                    "status": record["status"] or "",
                    "name_fr": record["name_fr"] or "",
                    "name_en": record["name_en"] or "",
                    "category": record["category"] or "",
                    "tags_fr": record["tags_fr"] or "",
                    "tags_en": record["tags_en"] or "",
                    "unit_fr": record["unit_fr"] or "",
                    "unit_en": record["unit_en"] or "",
                    "contributor": record["contributor"] or "",
                    "other_contributors": record["other_contributors"] or "",
                    "programme": record["programme"] or "",
                    "source": record["source"] or "",
                    "url": record["url"] or "",
                    "location": record["location"] or "",
                    "created_at": record["created_at"],  # Keep as datetime object
                    "modified_at": record["modified_at"],  # Keep as datetime object
                    "validity": record["validity"] or "",
                    "comments_fr": record["comments_fr"] or "",
                    "comments_en": record["comments_en"] or "",
                    "total": record["total"],
                    "co2f": record["co2f"],
                    "ch4f": record["ch4f"],
                    "ch4b": record["ch4b"],
                    "n2o": record["n2o"],
                    "extra_gases": record["extra_gases"],
                }
                
                # print(f"[Base Carbone] Document: {doc}")
                # logger.info(f"Base Carbone: Document: {doc}")

                documents.append(doc)
                count += 1
                
                if count % 1000 == 0:
                    print(f"[Base Carbone] Processed {count} factors...")
                    logger.info(f"Base Carbone: Processed {count} factors")
            
            print(f"[Base Carbone] Created {len(documents)} documents for indexing")
            logger.info(f"Base Carbone: Created {len(documents)} documents for indexing")
            
            # Validate minimum count (similar to map_invoices_to_base_carbone.py line 1730)
            if len(documents) < 50:
                warning_msg = f"⚠️ Only {len(documents)} factors loaded. Expected ~11,216 factors from Base Carbone v23.6."
                print(f"[Base Carbone] WARNING: {warning_msg}")
                logger.warning(warning_msg)
            
            # Process từng row: Build document → Generate embedding → Index
            print(f"[Base Carbone] Processing {len(documents)} rows sequentially (row → embedding → index)...")
            logger.info(f"Base Carbone: Processing {len(documents)} rows sequentially")
            
            index_name = SOLA_RAG_INDEX_NAME
            total_indexed = 0
            total_failed = 0
            
            # Initialize search client
            from azure.core.credentials import AzureKeyCredential
            from azure.search.documents import SearchClient
            
            search_client = SearchClient(
                endpoint=AZURE_SEARCH_ENDPOINT,
                index_name=index_name,
                credential=AzureKeyCredential(AZURE_SEARCH_KEY),
            )
            
            try:
                for doc in documents:
                    try:
                        # Generate embedding for this document
                        embedding = create_embedding_with_dimensions(doc["content"])
                        
                        # Build search document with cleaned values
                        doc_id = f"base_carbone_{doc.get('row_index', total_indexed)}"
                        search_doc = {
                            "id": doc_id,
                            "content": doc["content"],
                            "content_vector": embedding,
                            "row_index": clean_for_json(doc.get("row_index")),
                            "identifier": clean_for_json(doc.get("identifier")),
                            "status": clean_for_json(doc.get("status")) or "",
                            "name_fr": clean_for_json(doc.get("name_fr")) or "",
                            "name_en": clean_for_json(doc.get("name_en")) or "",
                            "category": clean_for_json(doc.get("category")) or "",
                            "tags_fr": clean_for_json(doc.get("tags_fr")) or "",
                            "tags_en": clean_for_json(doc.get("tags_en")) or "",
                            "unit_fr": clean_for_json(doc.get("unit_fr")) or "",
                            "unit_en": clean_for_json(doc.get("unit_en")) or "",
                            "contributor": clean_for_json(doc.get("contributor")) or "",
                            "other_contributors": clean_for_json(doc.get("other_contributors")) or "",
                            "programme": clean_for_json(doc.get("programme")) or "",
                            "source": clean_for_json(doc.get("source")) or "",
                            "url": clean_for_json(doc.get("url")) or "",
                            "location": clean_for_json(doc.get("location")) or "",
                            "created_at": clean_for_json(doc.get("created_at")),
                            "modified_at": clean_for_json(doc.get("modified_at")),
                            "validity": clean_for_json(doc.get("validity")) or "",
                            "comments_fr": clean_for_json(doc.get("comments_fr")) or "",
                            "comments_en": clean_for_json(doc.get("comments_en")) or "",
                            "total": clean_for_json(doc.get("total")),
                            "co2f": clean_for_json(doc.get("co2f")),
                            "ch4f": clean_for_json(doc.get("ch4f")),
                            "ch4b": clean_for_json(doc.get("ch4b")),
                            "n2o": clean_for_json(doc.get("n2o")),
                            "extra_gases": doc.get("extra_gases") or "[]",
                        }
                        
                        # Remove None values for numeric fields (Azure Search doesn't accept None for Edm.Double)
                        # But keep None for DateTimeOffset and Int32 fields (they accept None)
                        for key in ["total", "co2f", "ch4f", "ch4b", "n2o"]:
                            if search_doc.get(key) is None:
                                search_doc.pop(key, None)
                        
                        # Note: Don't validate JSON with json.dumps() because datetime objects
                        # are not JSON-serializable, but Azure Search SDK will handle them correctly
                        
                        # Index document to Azure AI Search
                        # TODO: Index document to Azure AI Search with batching
                        print(f"[Base Carbone] Indexing doc_id={doc_id} row_index={doc.get('row_index')} identifier={doc.get('identifier')} name_fr={doc.get('name_fr')} category={doc.get('category')}")
                        result = search_client.upload_documents(documents=[search_doc])
                        if result[0].succeeded:
                            total_indexed += 1
                            if total_indexed % 1000 == 0:
                                print(f"[Base Carbone] Indexed {total_indexed} factors...")
                                logger.info(f"Base Carbone: Indexed {total_indexed} factors")
                        else:
                            total_failed += 1
                            logger.warning(f"Base Carbone: Failed to index row {doc.get('row_index')}: {result[0].error_message}")
                            
                    except Exception as doc_error:
                        total_failed += 1
                        print(f"[Base Carbone] ERROR doc_id={doc_id if 'doc_id' in locals() else 'unknown'} row_index={doc.get('row_index')} err={doc_error}")
                        logger.error(f"Base Carbone: Error processing document row {doc.get('row_index')}: {doc_error}", exc_info=True)
                        continue
                
                print(f"[Base Carbone] SUCCESS: Indexed {total_indexed}/{len(documents)} documents to index '{index_name}' (failed: {total_failed})")
                logger.info(f"Base Carbone: Successfully indexed {total_indexed}/{len(documents)} documents to index '{index_name}' (failed: {total_failed})")
                
                return {
                    "status": "success",
                    "file": filename or excel_path.name,
                    "docs_indexed": total_indexed,
                    "total_docs": len(documents),
                    "failed": total_failed,
                    "index_name": index_name,
                }
                
            except Exception as e:
                error_msg = f"Error indexing documents to '{index_name}': {str(e)}"
                print(f"[Base Carbone] ERROR: {error_msg}")
                logger.error(f"Base Carbone: {error_msg}", exc_info=True)
                return {
                    "status": "error",
                    "error": error_msg,
                }
            
        except Exception as e:
            error_msg = f"Error processing Base Carbone Excel file: {str(e)}"
            print(f"[Base Carbone] ERROR: {error_msg}")
            logger.error(f"Base Carbone: {error_msg}", exc_info=True)
            return {
                "status": "error",
                "error": error_msg,
            }


# ============================================================
# SOLA RAG CHAT (LangChain)
# ============================================================
class SolaRagChat:
    """Chat agent for Sola RAG using LangChain RetrievalQA with Azure OpenAI and Azure AI Search"""
    
    def chat(
        self,
        question: str,
        rag_type: str = "sola",
        k: int = 5,
        filter_category: Optional[str] = None,
        filter_location: Optional[str] = None,
    ) -> Tuple[str, List[Dict], str]:
        """
        Perform retrieval + generation using LangChain RetrievalQA.
        Uses LLM_SYSTEM_PROMPT from sola_export.py for expert Base Carbone guidance.
        
        Args:
            question: User's question
            rag_type: "sola"
            k: top-k chunks to retrieve
            filter_category: Optional metadata filter by category
            filter_location: Optional metadata filter by location
        
        Returns:
            Tuple of (answer, sources, index_name)
            sources: List of dicts with source metadata (row_index, identifier, name_fr, name_en, etc.)
        """
        try:
            # Import LLM_SYSTEM_PROMPT from sola_export.py
            from companies.sdk.sola_export import LLM_SYSTEM_PROMPT
            
            # Validate rag_type
            if rag_type.lower() not in ["sola"]:
                logger.error(f"Invalid rag_type: {rag_type}")
                return (
                    f"Error: rag_type must be 'sola'",
                    [],
                    "",
                )
            
            # Get vector store
            vector_store = get_vector_store(rag_type.lower())
            index_name = SOLA_RAG_INDEX_NAME
            
            # Build search kwargs (exclude k - it's passed separately to as_retriever)
            search_kwargs: Dict[str, Any] = {}
            
            # Build OData filter string for Azure Search
            filter_parts = []
            if filter_category:
                filter_parts.append(f"category eq '{filter_category}'")
            if filter_location:
                filter_parts.append(f"location eq '{filter_location}'")
            
            if filter_parts:
                search_kwargs["filter"] = " and ".join(filter_parts)
            
            # STEP 1: Fast Retrieval (NO CROSS-ATTENTION)
            # Retrieve many candidate chunks quickly (top 20-50)
            # This is fast but not deeply accurate - uses cosine similarity only
            try:
                from companies.sdk.rag_reranker import rerank_chunks
                from langchain.schema import Document
                from langchain.schema.retriever import BaseRetriever
                from pydantic import Field
                from typing import List
                
                # ============================================================
                # STEP 1: FAST RETRIEVAL (NO CROSS-ATTENTION)
                # ============================================================
                logger.info(f"[SOLA RAG] =========================================")
                logger.info(f"[SOLA RAG] STEP 1: FAST RETRIEVAL (NO CROSS-ATTENTION)")
                logger.info(f"[SOLA RAG] Goal: Retrieve many candidate chunks quickly")
                logger.info(f"[SOLA RAG] Method: Cosine similarity (vector search)")
                logger.info(f"[SOLA RAG] Target: Top 30 candidates (range: 20-50)")
                
                logger.info(f"[SOLA RAG] Step 1: Retrieving documents for reranking...")
                # Use similarity_search_with_score to get more candidates
                # IMPORTANT: Do NOT pass filter as explicit keyword argument
                # LangChain's similarity_search_with_score internally passes kwargs to search(),
                # and if filter is both explicit and in kwargs, we get "multiple values for keyword argument 'filter'"
                # Solution: Pass filter ONLY through search_kwargs, not as explicit parameter
                retrieved_docs_with_scores = vector_store.similarity_search_with_score(
                    question,
                    k=30,  # Retrieve top 30-50 for reranking (as per RAG flow)
                    **(search_kwargs if search_kwargs else {}),  # Pass all kwargs including filter
                )
                logger.info(f"[SOLA RAG] Step 1: ✅ Fast Retrieval completed - Retrieved {len(retrieved_docs_with_scores)} candidate chunks")
                logger.info(f"[SOLA RAG] Step 1: Method: Cosine similarity (no cross-attention)")
                
                if retrieved_docs_with_scores:
                    # Prepare chunks for reranking
                    chunks_for_reranking = []
                    for doc, score in retrieved_docs_with_scores:
                        chunk_data = {
                            "content": doc.page_content,
                            "metadata": doc.metadata,
                            "vector_score": float(score) if score else 0.0,
                        }
                        chunks_for_reranking.append(chunk_data)
                    
                    # ============================================================
                    # STEP 2: METADATA / ENTITY FILTERING
                    # ============================================================
                    logger.info(f"[SOLA RAG] =========================================")
                    logger.info(f"[SOLA RAG] STEP 2: METADATA / ENTITY FILTERING")
                    logger.info(f"[SOLA RAG] Goal: Reduce noise before expensive models")
                    logger.info(f"[SOLA RAG] Filter: category, location (via search_kwargs)")
                    logger.info(f"[SOLA RAG] Step 2: ✅ Metadata filtering completed - {len(chunks_for_reranking)} chunks remaining")
                    
                    # ============================================================
                    # STEP 3: RE-RANKING (CROSS-ATTENTION LEVEL 1)
                    # ============================================================
                    logger.info(f"[SOLA RAG] =========================================")
                    logger.info(f"[SOLA RAG] STEP 3: RE-RANKING (CROSS-ATTENTION LEVEL 1)")
                    logger.info(f"[SOLA RAG] Goal: Let the query read each chunk and score relevance")
                    logger.info(f"[SOLA RAG] Method: Cross-Encoder (sentence-transformers)")
                    logger.info(f"[SOLA RAG] Input: {len(chunks_for_reranking)} chunks to rerank")
                    logger.info(f"[SOLA RAG] Output: Top 5 chunks (range: 3-5)")
                    
                    logger.info(f"[SOLA RAG] Step 3: Starting Cross-Encoder reranking...")
                    top_chunks, all_ranked_chunks = rerank_chunks(
                        query=question,
                        chunks=chunks_for_reranking,
                        top_k=5,  # Get top 3-5 as per RAG flow
                        content_field="content",
                    )
                    
                    # Log reranking results safely
                    if top_chunks:
                        top1_score = top_chunks[0].get('rerank_score', 0.0) if top_chunks else 0.0
                        top3_score = top_chunks[2].get('rerank_score', 0.0) if len(top_chunks) > 2 else 0.0
                        top5_score = top_chunks[4].get('rerank_score', 0.0) if len(top_chunks) > 4 else 0.0
                        logger.info(f"[SOLA RAG] Step 3: ✅ Cross-Attention Level 1 completed")
                        logger.info(f"[SOLA RAG] Step 3: Top 1 score: {top1_score:.4f}, Top 3 score: {top3_score:.4f}, Top 5 score: {top5_score:.4f}")
                        logger.info(f"[SOLA RAG] Step 3: Selected {len(top_chunks)} chunks for prompt construction")
                    else:
                        logger.info(f"[SOLA RAG] Step 3: ✅ Reranking completed - no chunks returned")
                    
                    # Convert reranked chunks back to LangChain Documents
                    reranked_docs = []
                    for chunk in top_chunks[:5]:  # Top 3-5 as per RAG flow
                        doc = Document(
                            page_content=chunk["content"],
                            metadata=chunk.get("metadata", {})
                        )
                        reranked_docs.append(doc)
                    
                    # Create custom retriever that returns only top reranked documents
                    # BaseRetriever is a Pydantic model, so we need to properly define fields
                    from pydantic import Field, ConfigDict
                    
                    class RerankedRetriever(BaseRetriever):
                        """Custom retriever that returns pre-reranked documents"""
                        # Use model_config to allow arbitrary types for Document
                        model_config = ConfigDict(arbitrary_types_allowed=True)
                        top_docs: List[Document] = Field(default_factory=list, description="Pre-reranked documents to return")
                        
                        def __init__(self, top_docs: List[Document], **kwargs):
                            # Use super().__init__ to properly initialize Pydantic model
                            super().__init__(top_docs=top_docs, **kwargs)
                        
                        def get_relevant_documents(self, query: str):
                            return self.top_docs
                        
                        async def aget_relevant_documents(self, query: str):
                            return self.top_docs
                    
                    # Use reranked retriever
                    retriever = RerankedRetriever(reranked_docs)
                    logger.info(f"[SOLA RAG] Using reranked retriever with {len(reranked_docs)} documents (top 3-5 as per RAG flow)")
                else:
                    logger.warning(f"[SOLA RAG] No documents retrieved, using original retriever")
                    retriever = vector_store.as_retriever(search_kwargs=search_kwargs, k=k)
            except Exception as rerank_exc:
                logger.warning(f"[SOLA RAG] Step 3: ⚠️ Reranking failed: {rerank_exc}, using original retriever")
                logger.exception(rerank_exc)
                # Fallback: use original retriever with k=5
            retriever = vector_store.as_retriever(search_kwargs=search_kwargs, k=k)
            
            # ============================================================
            # STEP 4: PROMPT CONSTRUCTION
            # ============================================================
            logger.info(f"[SOLA RAG] =========================================")
            logger.info(f"[SOLA RAG] STEP 4: PROMPT CONSTRUCTION")
            logger.info(f"[SOLA RAG] Goal: Force the LLM to answer using only provided context")
            logger.info(f"[SOLA RAG] Method: LangChain PromptTemplate + Retrieved context")
            
            # Build prompt template with LLM_SYSTEM_PROMPT
            # LangChain RetrievalQA uses {context} and {question} placeholders
            # Need to escape all curly braces in LLM_SYSTEM_PROMPT except {context} and {question}
            # Replace { with {{ and } with }}, then restore {context} and {question}
            escaped_system_prompt = LLM_SYSTEM_PROMPT.replace("{", "{{").replace("}", "}}")
            # Restore the actual placeholders we need
            escaped_system_prompt = escaped_system_prompt.replace("{{context}}", "{context}").replace("{{question}}", "{question}")
            
            prompt_template = f"""{escaped_system_prompt}

                Use the following pieces of context from ADEME Base Carbone v23.6 to answer the question.
                If you don't know the answer based on the context, say that you don't know.

                Context:
                {{context}}

                Question: {{question}}

                Answer:
            """
            
            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )
            
            logger.info(f"[SOLA RAG] Step 4: Prompt template constructed with system prompt")
            logger.info(f"[SOLA RAG] Step 4: ✅ Prompt construction completed")
            
            # ============================================================
            # STEP 5: ANSWER GENERATION (CROSS-ATTENTION LEVEL 2)
            # ============================================================
            logger.info(f"[SOLA RAG] =========================================")
            logger.info(f"[SOLA RAG] STEP 5: ANSWER GENERATION (CROSS-ATTENTION LEVEL 2)")
            logger.info(f"[SOLA RAG] Goal: Generate answer grounded in retrieved documents")
            logger.info(f"[SOLA RAG] Method: LangChain LLM with cross-attention to context")
            logger.info(f"[SOLA RAG] Step 5: Starting LLM generation with cross-attention...")
            
            # Build RAG chain (retriever + llm) with custom prompt
            # Use lazy-initialized LLM to avoid base_url/azure_endpoint conflict
            qa_chain = RetrievalQA.from_chain_type(
                llm=get_llm(),
                retriever=retriever,
                return_source_documents=True,
                chain_type_kwargs={"prompt": prompt},  # Use custom prompt with LLM_SYSTEM_PROMPT
            )
            
            # Execute using invoke (recommended) instead of deprecated __call__
            result = qa_chain.invoke({"query": question})
            
            logger.info(f"[SOLA RAG] Step 5: LLM response received")
            
            # result["result"] = final answer
            # result["source_documents"] = list[Document] used as evidence
            # Convert sources to references format
            references = []
            seen_identifiers = set()
            
            for doc in result.get("source_documents", []):
                meta = doc.metadata or {}
                identifier = meta.get("identifier")
                
                # Skip duplicates
                if identifier and identifier in seen_identifiers:
                    continue
                if identifier:
                    seen_identifiers.add(identifier)
                
                # Build source reference
                references.append({
                    "row_index": meta.get("row_index"),
                    "identifier": identifier,
                    "name_fr": meta.get("name_fr", ""),
                    "name_en": meta.get("name_en", ""),
                    "category": meta.get("category", ""),
                    "unit_fr": meta.get("unit_fr", ""),
                    "unit_en": meta.get("unit_en", ""),
                    "total": meta.get("total"),
                    "location": meta.get("location", ""),
                })
            
            answer = result.get("result", "I apologize, but I couldn't generate a response. Please try again.")
            
            logger.info(f"[SOLA RAG] Step 5: ✅ Cross-Attention Level 2 completed")
            logger.info(f"[SOLA RAG] Step 5: Answer length: {len(answer)} characters")
            logger.info(f"[SOLA RAG] Step 5: References extracted: {len(references)}")
            logger.info(f"[SOLA RAG] =========================================")
            logger.info(f"[SOLA RAG] ✅ RAG FLOW COMPLETED - All 5 steps executed")
            logger.info(f"[SOLA RAG] Summary:")
            logger.info(f"[SOLA RAG]   Step 1: Fast Retrieval (NO CROSS-ATTENTION) - Cosine similarity")
            logger.info(f"[SOLA RAG]   Step 2: Metadata / Entity Filtering")
            logger.info(f"[SOLA RAG]   Step 3: Re-ranking (CROSS-ATTENTION LEVEL 1) - Cross-Encoder")
            logger.info(f"[SOLA RAG]   Step 4: Prompt Construction")
            logger.info(f"[SOLA RAG]   Step 5: Answer Generation (CROSS-ATTENTION LEVEL 2) - LLM")
            logger.info(f"[SOLA RAG] Answer ready with {len(references)} references")
            logger.info(f"[SOLA RAG] =========================================")
            
            return answer, references, index_name
            
        except Exception as e:
            logger.error(f"Error in Sola RAG chat: {e}", exc_info=True)
            return (
                f"I encountered an error: {str(e)}",
                [],
                "",
            )


# ============================================================
# SOLA RAG CSV/XLSX UPLOAD PROCESSOR (LangChain)
# ============================================================
class SolaRagCsvProcessor:
    """Process CSV/XLSX files: Parse → Embedding → Indexing using LangChain"""
    
    def upload_csv(
        self,
        csv_file_path: str,
        filename: str,
        rag_type: str = "sola",
        blob_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Ingest a CSV or XLSX file and index into Azure AI Search using LangChain.
        For Base Carbone data, use BaseCarboneExcelProcessor.upload_base_carbone_excel() instead.
        
        Args:
            csv_file_path: Path to CSV or XLSX file
            filename: Original file name
            rag_type: "sola"
            blob_name: Optional blob name for storage
        
        Returns:
            Dict with status, file info, and indexing results
        """
        try:
            print(f"[Sola RAG] Starting upload for file {filename} (path: {csv_file_path})")
            logger.info(f"Sola RAG: Starting upload for file {filename} (path: {csv_file_path})")
            
            # Load CSV or XLSX into DataFrame
            file_ext = filename.lower()
            try:
                if file_ext.endswith('.xlsx'):
                    df = pd.read_excel(csv_file_path, engine='openpyxl')
                elif file_ext.endswith('.csv'):
                    try:
                        df = pd.read_csv(csv_file_path, encoding='utf-8')
                    except UnicodeDecodeError:
                        try:
                            df = pd.read_csv(csv_file_path, encoding='latin-1')
                        except UnicodeDecodeError:
                            df = pd.read_csv(csv_file_path, encoding='iso-8859-1')
                else:
                    return {
                        "status": "error",
                        "error": f"Unsupported file type. Only CSV and XLSX files are supported.",
                    }
            except Exception as e:
                return {
                    "status": "error",
                    "error": f"Failed to read file: {str(e)}",
                }
            
            if df.empty:
                return {
                    "status": "error",
                    "error": "File is empty",
                }
            
            print(f"[Sola RAG] Loaded file {filename} with {len(df)} rows")
            logger.info(f"Sola RAG: Loaded file {filename} with {len(df)} rows")
            
            # Normalize column names
            df.columns = df.columns.str.lower().str.strip()
            
            # Initialize search client (một lần cho tất cả rows)
            index_name = SOLA_RAG_INDEX_NAME
            from azure.core.credentials import AzureKeyCredential
            from azure.search.documents import SearchClient
            
            search_client = SearchClient(
                endpoint=AZURE_SEARCH_ENDPOINT,
                index_name=index_name,
                credential=AzureKeyCredential(AZURE_SEARCH_KEY),
                
            )
            
            # Process từng row: Build document → Generate embedding → Index
            print(f"[Sola RAG] Processing {len(df)} rows sequentially (row → embedding → index)...")
            logger.info(f"Sola RAG: Processing {len(df)} rows sequentially")
            
            total_indexed = 0
            total_failed = 0
            
            try:
                for idx, row in df.iterrows():
                    try:
                        # Build content text from row data
                        content_parts = []
                        for col in df.columns:
                            value = row.get(col)
                            if pd.notna(value) and str(value).strip():
                                content_parts.append(f"{col}: {value}")
                        
                        content_text = ". ".join(content_parts) + "."
                        
                        # Build metadata
                        metadata = {
                            "row_index": int(idx) + 1,  # 1-based
                            "filename": filename,
                        }
                        
                        # Add all row data as metadata (only Base Carbone fields that exist in schema)
                        for col in df.columns:
                            value = row.get(col)
                            if pd.notna(value):
                                # Only include Base Carbone schema fields
                                if col in ["identifier", "status", "name_fr", "name_en", "category", "tags_fr", "tags_en",
                                          "unit_fr", "unit_en", "contributor", "programme", "source", "url", "location",
                                          "total", "co2f", "ch4f", "ch4b", "n2o"]:
                                    if col in ["identifier", "row_index"]:
                                        try:
                                            metadata[col] = int(value) if value else 0
                                        except:
                                            metadata[col] = str(value)
                                    elif col in ["total", "co2f", "ch4f", "ch4b", "n2o"]:
                                        try:
                                            metadata[col] = float(value) if value else None
                                        except:
                                            metadata[col] = str(value)
                                    else:
                                        metadata[col] = str(value) if value else ""
                        
                        # Generate embedding for this document
                        embedding = create_embedding_with_dimensions(content_text)
                        
                        # Build search document (doc_id must be URL-safe for Azure Search)
                        doc_id = f"sola_{sanitize_key(str(metadata['row_index']))}"
                        search_doc = {
                            "id": doc_id,
                            "content": content_text,
                            "content_vector": embedding,
                            **metadata,  # Only fields already filtered to match schema
                        }
                        
                        # Index document to Azure AI Search (từng document một)
                        print(f"[Sola RAG] Indexing doc_id={doc_id}")
                        result = search_client.upload_documents(documents=[search_doc])
                        if result[0].succeeded:
                            total_indexed += 1
                            if total_indexed % 100 == 0:
                                print(f"[Sola RAG] Indexed {total_indexed} rows...")
                                logger.info(f"Sola RAG: Indexed {total_indexed} rows")
                        else:
                            total_failed += 1
                            logger.warning(f"Sola RAG: Failed to index row {metadata['row_index']}: {result[0].error_message}")
                            
                    except Exception as row_error:
                        total_failed += 1
                        print(f"[Sola RAG] ERROR doc_id={doc_id if 'doc_id' in locals() else 'unknown'} row_index={metadata.get('row_index','?')} err={row_error}")
                        logger.error(f"Sola RAG: Error processing row {idx}: {row_error}", exc_info=True)
                        continue
                
                print(f"[Sola RAG] SUCCESS: Indexed {total_indexed}/{len(df)} rows to index '{index_name}' (failed: {total_failed})")
                logger.info(f"Sola RAG: Successfully indexed {total_indexed}/{len(df)} rows to index '{index_name}' (failed: {total_failed})")
                
                return {
                    "status": "success",
                    "file": filename,
                    "docs_indexed": total_indexed,
                    "total_rows": len(df),
                    "failed": total_failed,
                    "index_name": index_name,
                }
                
            except Exception as e:
                error_msg = f"Error indexing documents: {str(e)}"
                logger.error(f"Sola RAG: {error_msg}", exc_info=True)
                return {
                    "status": "error",
                    "error": error_msg,
                }
            
        except Exception as e:
            error_msg = f"Error processing file: {str(e)}"
            logger.error(f"Sola RAG: {error_msg}", exc_info=True)
            return {
                "status": "error",
                "error": error_msg,
            }
