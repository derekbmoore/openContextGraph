"""
Antigravity Ingestion Router (ctxEco-Lib)

MISSION: Defy data gravity by routing ingestion based on "Truth Value".

Classification System:
- Class A (Immutable Truth): High-fidelity extraction via Docling
- Class B (Ephemeral Stream): Semantic chunking via Unstructured
- Class C (Operational Pulse): Native handling via Pandas

OpenContextGraph - ETL Layer
NIST AI RMF: MAP 1.5 (Boundaries), MANAGE 2.3 (Data Governance)
"""

import logging
import uuid
import os
from enum import Enum
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class DataClass(str, Enum):
    """Data classification for Antigravity ingestion routing."""
    CLASS_A_TRUTH = "immutable_truth"
    CLASS_B_CHATTER = "ephemeral_stream"
    CLASS_C_OPS = "operational_pulse"


# File type mappings
CLASS_A_EXTENSIONS = {'.pdf', '.scidoc'}
CLASS_B_EXTENSIONS = {'.pptx', '.docx', '.doc', '.eml', '.msg', '.html', '.md', '.txt'}
CLASS_C_EXTENSIONS = {'.csv', '.parquet', '.json', '.log', '.jsonl', '.xlsx'}

# Keywords indicating technical/immutable content
TRUTH_KEYWORDS = {
    'manual', 'spec', 'specification', 'standard', 'iso', 'safety',
    'protocol', 'procedure', 'guideline', 'regulation', 'compliance',
    'datasheet', 'technical', 'engineering', 'reference'
}


class AntigravityRouter:
    """
    Routes documents to appropriate extraction engines based on Truth Value.
    
    The router classifies documents and delegates to:
    - DoclingEngine: High-fidelity extraction (tables, layouts)
    - UnstructuredEngine: Semantic chunking for narrative content
    - PandasEngine: Native structured data handling
    
    NIST AI RMF: MANAGE 2.3 - Classification determines governance rules
    """
    
    def __init__(
        self, 
        fallback_to_unstructured: bool = True,
        docling_enabled: bool = False
    ):
        """
        Initialize the router.
        
        Args:
            fallback_to_unstructured: If True, Class A files fall back
                                      to Unstructured when Docling unavailable.
            docling_enabled: Whether Docling is available (requires license)
        """
        self.fallback_to_unstructured = fallback_to_unstructured
        self.docling_enabled = docling_enabled or os.getenv("DOCLING_ENABLED", "false").lower() == "true"
    
    def classify(self, file_path: str) -> Tuple[DataClass, str]:
        """
        Classify a file into a Data Class.
        
        NIST AI RMF: MANAGE 2.3 - Classification is first governance step
        
        Args:
            file_path: Path to the file
        
        Returns:
            Tuple of (DataClass, classification_reason)
        """
        path = Path(file_path)
        ext = path.suffix.lower()
        filename_lower = path.name.lower()
        
        # Extension-based classification
        if ext in CLASS_A_EXTENSIONS:
            return DataClass.CLASS_A_TRUTH, f"Extension {ext} indicates technical document"
        
        if ext in CLASS_C_EXTENSIONS:
            return DataClass.CLASS_C_OPS, f"Extension {ext} indicates operational data"
        
        if ext in CLASS_B_EXTENSIONS:
            # Check for technical keywords in filename
            if self._is_technical_document(filename_lower):
                return DataClass.CLASS_A_TRUTH, "Filename keywords indicate technical document"
            return DataClass.CLASS_B_CHATTER, f"Extension {ext} indicates ephemeral content"
        
        # Default to Class B for unknown types
        return DataClass.CLASS_B_CHATTER, "Unknown file type, defaulting to ephemeral"
    
    def _is_technical_document(self, filename: str) -> bool:
        """
        Determine if a document is likely technical/immutable.
        
        Uses filename heuristics. Could be extended with:
        - First-page text analysis
        - Metadata extraction
        - ML classification
        """
        return any(keyword in filename for keyword in TRUTH_KEYWORDS)
    
    async def ingest(
        self,
        file_path: str,
        filename: Optional[str] = None,
        force_class: Optional[DataClass] = None,
        user_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Ingest a document through the appropriate engine.
        
        NIST AI RMF Controls:
        - MAP 1.5: Provenance preserved in chunk metadata
        - MANAGE 2.3: Classification determines processing
        - MEASURE 2.1: Extraction quality can be audited
        
        Args:
            file_path: Path to the document
            filename: Optional display name
            force_class: Override automatic classification
            user_id: User performing the ingestion
            tenant_id: Tenant for data isolation
        
        Returns:
            List of chunks with text and metadata
        """
        # Classify
        if force_class:
            data_class = force_class
            reason = "Forced classification"
        else:
            data_class, reason = self.classify(file_path)
        
        logger.info(
            f"Antigravity: Classified '{filename or file_path}' as {data_class.value} "
            f"({reason})"
        )
        
        # Generate provenance ID
        provenance_id = f"{data_class.value[0]}-{uuid.uuid4().hex[:8]}"
        
        # Route to engine
        chunks = await self._execute_engine(file_path, filename or file_path, data_class)
        
        # Add metadata to all chunks
        now = datetime.now(timezone.utc).isoformat()
        for chunk in chunks:
            chunk["metadata"] = chunk.get("metadata", {})
            chunk["metadata"].update({
                "provenance_id": provenance_id,
                "data_class": data_class.value,
                "source_file": filename or Path(file_path).name,
                "ingested_at": now,
                "decay_rate": self._get_decay_rate(data_class),
                "user_id": user_id,
                "tenant_id": tenant_id,
            })
        
        logger.info(
            f"Antigravity: Extracted {len(chunks)} chunks from "
            f"'{filename or file_path}' (provenance: {provenance_id})"
        )
        
        return chunks
    
    async def ingest_bytes(
        self,
        content: bytes,
        filename: str,
        force_class: Optional[DataClass] = None,
        user_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Ingest document from bytes (e.g., from file upload).
        
        Writes to temp file and processes.
        """
        import tempfile
        
        # Determine extension from filename
        ext = Path(filename).suffix
        
        # Write to temp file
        with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        
        try:
            return await self.ingest(
                file_path=tmp_path,
                filename=filename,
                force_class=force_class,
                user_id=user_id,
                tenant_id=tenant_id,
            )
        finally:
            # Clean up temp file
            try:
                Path(tmp_path).unlink()
            except Exception:
                pass
    
    async def _execute_engine(
        self,
        file_path: str,
        filename: str,
        data_class: DataClass,
    ) -> List[Dict[str, Any]]:
        """Execute the appropriate extraction engine."""
        
        if data_class == DataClass.CLASS_A_TRUTH:
            # High-fidelity extraction for technical documents
            if self.docling_enabled:
                try:
                    return await self._extract_with_docling(file_path)
                except Exception as e:
                    logger.warning(f"Docling failed: {e}")
                    if not self.fallback_to_unstructured:
                        raise
            
            # Fall back to Unstructured
            return await self._extract_with_unstructured(file_path)
        
        elif data_class == DataClass.CLASS_B_CHATTER:
            # Semantic chunking for narrative content
            return await self._extract_with_unstructured(file_path)
        
        elif data_class == DataClass.CLASS_C_OPS:
            # Native structured data handling
            return await self._extract_with_pandas(file_path)
        
        else:
            raise ValueError(f"Unknown data class: {data_class}")
    
    async def _extract_with_docling(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Extract with Docling for high-fidelity tables and layouts.
        
        Docling (IBM) provides:
        - TableFormer for table reconstruction
        - Bounding box coordinates for provenance
        - Multi-column layout preservation
        """
        try:
            from docling.document_converter import DocumentConverter
            
            converter = DocumentConverter()
            result = converter.convert(file_path)
            
            chunks = []
            for element in result.document.elements:
                chunks.append({
                    "text": element.text,
                    "metadata": {
                        "element_type": element.type,
                        "page": getattr(element, "page_number", None),
                        "bbox": getattr(element, "bbox", None),
                    }
                })
            
            return chunks
            
        except ImportError:
            logger.warning("Docling not installed, falling back to Unstructured")
            return await self._extract_with_unstructured(file_path)
    
    async def _extract_with_unstructured(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Extract with Unstructured for semantic chunking.
        
        Unstructured.io provides:
        - Header-based splitting
        - Element type detection (title, narrative, table)
        - Metadata extraction
        """
        try:
            from unstructured.partition.auto import partition
            
            elements = partition(filename=file_path)
            
            return [
                {
                    "text": str(element),
                    "metadata": {
                        "element_type": element.category,
                    }
                }
                for element in elements
                if str(element).strip()
            ]
            
        except ImportError:
            logger.warning("Unstructured not installed, using simple text extraction")
            return await self._extract_simple(file_path)
        except Exception as e:
            logger.error(f"Unstructured extraction failed: {e}")
            return await self._extract_simple(file_path)
    
    async def _extract_with_pandas(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Extract with Pandas for structured data.
        
        Preserves column structure and types.
        Converts to vector-ready format.
        """
        try:
            import pandas as pd
        except ImportError:
            logger.warning("Pandas not installed")
            return []
        
        ext = Path(file_path).suffix.lower()
        
        try:
            if ext == '.csv':
                df = pd.read_csv(file_path)
            elif ext == '.parquet':
                df = pd.read_parquet(file_path)
            elif ext in ('.json', '.jsonl'):
                df = pd.read_json(file_path, lines=(ext == '.jsonl'))
            elif ext == '.xlsx':
                df = pd.read_excel(file_path)
            else:
                return []
            
            # Convert each row to a chunk
            chunks = []
            for idx, row in df.iterrows():
                chunks.append({
                    "text": row.to_json(),
                    "metadata": {
                        "row_index": idx,
                        "columns": list(df.columns),
                    }
                })
            
            return chunks
            
        except Exception as e:
            logger.error(f"Pandas extraction failed: {e}")
            return []
    
    async def _extract_simple(self, file_path: str) -> List[Dict[str, Any]]:
        """Simple text extraction fallback."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Simple paragraph splitting
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            
            return [
                {"text": p, "metadata": {"element_type": "text"}}
                for p in paragraphs
            ]
            
        except Exception as e:
            logger.error(f"Simple extraction failed: {e}")
            return []
    
    def _get_decay_rate(self, data_class: DataClass) -> float:
        """
        Get decay rate based on classification.
        
        Decay rate determines how quickly information
        loses relevance over time.
        
        0.0 = Permanent (never decays)
        1.0 = Ephemeral (rapid decay)
        """
        decay_rates = {
            DataClass.CLASS_A_TRUTH: 0.01,   # Nearly permanent
            DataClass.CLASS_B_CHATTER: 0.5,  # Moderate decay
            DataClass.CLASS_C_OPS: 0.9,       # Rapid decay
        }
        return decay_rates.get(data_class, 0.5)


# Singleton instance
_router: Optional[AntigravityRouter] = None


def get_antigravity_router() -> AntigravityRouter:
    """Get the singleton router instance."""
    global _router
    if _router is None:
        _router = AntigravityRouter()
    return _router


# Convenience alias
antigravity_router = property(lambda self: get_antigravity_router())
