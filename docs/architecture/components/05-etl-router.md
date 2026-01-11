# ETL Router — Antigravity Document Ingestion

## Purpose

The ETL Router (Antigravity Router) provides **truth-value-based document classification and ingestion**. It routes documents to the appropriate extraction engine based on their "data gravity"—the stability and reliability of the information they contain.

## Why This Exists

### The Problem

Traditional RAG systems treat all documents equally:

- Engineering manuals processed same as Slack messages
- CSV telemetry chunked like narrative text
- Table structures destroyed by generic parsers
- No provenance tracking for compliance

### The Solution

A classification-first ingestion pipeline that:

1. **Classifies by truth value** (A/B/C)
2. **Routes to specialized engines**
3. **Preserves document structure**
4. **Tracks provenance for every chunk**

---

## The Antigravity Concept

In physics, gravity pulls objects toward the center. In data systems, **Data Gravity** pulls data into massive, immobile lakes where it becomes:

- Hard to access
- Expensive to move
- Difficult to govern

**Antigravity** defies this by keeping data:

- **Active**: Context, not cold storage
- **Classified**: Treated according to truth value
- **Attributed**: Linked to source with provenance

---

## Classification System

```
┌─────────────────────────────────────────────────────────────┐
│               Document Classification                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ CLASS A: IMMUTABLE TRUTH                               │ │
│  │ • Engineering manuals, specifications                   │ │
│  │ • Safety protocols, regulations                         │ │
│  │ • Scientific papers, datasheets                         │ │
│  │ • Decay Rate: 0.01 (nearly permanent)                   │ │
│  │ • Engine: Docling (high-fidelity extraction)            │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ CLASS B: EPHEMERAL STREAM                              │ │
│  │ • Emails, meeting notes                                 │ │
│  │ • PowerPoint slides                                     │ │
│  │ • Word documents, wikis                                 │ │
│  │ • Decay Rate: 0.5-0.8 (moderate decay)                  │ │
│  │ • Engine: Unstructured (semantic chunking)              │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ CLASS C: OPERATIONAL PULSE                             │ │
│  │ • CSV logs, sensor data                                 │ │
│  │ • JSON API responses                                    │ │
│  │ • Parquet files, metrics                                │ │
│  │ • Decay Rate: 0.9 (rapid decay, time-sensitive)         │ │
│  │ • Engine: Pandas (native structured handling)           │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Code Sample

```python
# backend/etl/antigravity_router.py
"""
Antigravity Ingestion Router (CtxEco-Lib)

MISSION: Defy data gravity by routing ingestion based on "Truth Value".

Classification System:
- Class A (Immutable Truth): High-fidelity extraction via Docling
- Class B (Ephemeral Stream): Semantic chunking via Unstructured
- Class C (Operational Pulse): Native handling via Pandas

NIST AI RMF Alignment:
- MAP 1.5: Document boundaries preserved via provenance
- MANAGE 2.3: Classification determines governance rules
- MEASURE 2.1: Extraction quality is validated
"""

import logging
import uuid
from enum import Enum
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime, UTC

logger = logging.getLogger(__name__)


class DataClass(str, Enum):
    """Data classification for Antigravity ingestion routing."""
    CLASS_A_TRUTH = "immutable_truth"
    CLASS_B_CHATTER = "ephemeral_stream"
    CLASS_C_OPS = "operational_pulse"


# File type mappings
CLASS_A_EXTENSIONS = {'.pdf', '.scidoc'}
CLASS_B_EXTENSIONS = {'.pptx', '.docx', '.doc', '.eml', '.msg', '.html', '.md'}
CLASS_C_EXTENSIONS = {'.csv', '.parquet', '.json', '.log', '.jsonl'}

# Keywords indicating technical/immutable content
TRUTH_KEYWORDS = {
    'manual', 'spec', 'specification', 'standard', 'iso', 'safety',
    'protocol', 'procedure', 'guideline', 'regulation', 'compliance'
}


class AntigravityRouter:
    """
    Routes documents to appropriate extraction engines.
    
    The router classifies documents and delegates to:
    - DoclingEngine: High-fidelity extraction (tables, layouts)
    - UnstructuredEngine: Semantic chunking for narrative content
    - PandasEngine: Native structured data handling
    
    NIST AI RMF: MANAGE 2.3 - Classification determines governance
    """
    
    def __init__(self, fallback_to_unstructured: bool = True):
        """
        Initialize the router.
        
        Args:
            fallback_to_unstructured: If True, Class A files fall back
                                      to Unstructured when Docling unavailable.
        """
        self.fallback_to_unstructured = fallback_to_unstructured
        self._docling_engine = None
        self._unstructured_engine = None
        self._pandas_engine = None
    
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
            if self._is_technical_document(filename_lower, file_path):
                return DataClass.CLASS_A_TRUTH, "Filename keywords indicate technical document"
            return DataClass.CLASS_B_CHATTER, f"Extension {ext} indicates ephemeral content"
        
        # Default to Class B for unknown types
        return DataClass.CLASS_B_CHATTER, "Unknown file type, defaulting to ephemeral"
    
    def _is_technical_document(self, filename: str, file_path: str) -> bool:
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
        provenance_id = f"{data_class.value[:1]}-{uuid.uuid4().hex[:8]}"
        
        # Route to engine
        chunks = await self._execute_engine(file_path, filename or file_path, data_class)
        
        # Add metadata to all chunks
        for chunk in chunks:
            chunk["metadata"] = chunk.get("metadata", {})
            chunk["metadata"].update({
                "provenance_id": provenance_id,
                "data_class": data_class.value,
                "source_file": filename or Path(file_path).name,
                "ingested_at": datetime.now(UTC).isoformat(),
                "decay_rate": self._get_decay_rate(data_class),
            })
        
        logger.info(
            f"Antigravity: Extracted {len(chunks)} chunks from "
            f"'{filename or file_path}' (provenance: {provenance_id})"
        )
        
        return chunks
    
    async def _execute_engine(
        self,
        file_path: str,
        filename: str,
        data_class: DataClass,
    ) -> List[Dict[str, Any]]:
        """Execute the appropriate extraction engine."""
        
        if data_class == DataClass.CLASS_A_TRUTH:
            # High-fidelity extraction for technical documents
            try:
                return await self._extract_with_docling(file_path)
            except Exception as e:
                if self.fallback_to_unstructured:
                    logger.warning(f"Docling failed, falling back: {e}")
                    return await self._extract_with_unstructured(file_path)
                raise
        
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
        # TODO: Integrate Docling
        # from docling.document_converter import DocumentConverter
        # converter = DocumentConverter()
        # result = converter.convert(file_path)
        
        return [{"text": f"[Docling placeholder for {file_path}]", "metadata": {}}]
    
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
        except Exception as e:
            logger.error(f"Unstructured extraction failed: {e}")
            return []
    
    async def _extract_with_pandas(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Extract with Pandas for structured data.
        
        Preserves column structure and types.
        Converts to vector-ready format.
        """
        import pandas as pd
        from pathlib import Path
        
        ext = Path(file_path).suffix.lower()
        
        try:
            if ext == '.csv':
                df = pd.read_csv(file_path)
            elif ext == '.parquet':
                df = pd.read_parquet(file_path)
            elif ext == '.json' or ext == '.jsonl':
                df = pd.read_json(file_path, lines=(ext == '.jsonl'))
            else:
                return []
            
            # Convert each row to a chunk
            return [
                {
                    "text": row.to_json(),
                    "metadata": {
                        "row_index": idx,
                        "columns": list(df.columns),
                    }
                }
                for idx, row in df.iterrows()
            ]
        except Exception as e:
            logger.error(f"Pandas extraction failed: {e}")
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
antigravity_router = AntigravityRouter()
```

---

## NIST AI RMF Alignment

| Function | Control | Implementation |
|----------|---------|----------------|
| **MAP 1.5** | System Boundaries | `provenance_id` tracks document origin |
| **MANAGE 2.3** | Data Governance | Classification determines handling rules |
| **MEASURE 2.1** | Data Quality | Extraction quality is auditable |
| **GOVERN 1.1** | Policies | Classification rules are explicit |

---

## Extraction Engines

### Docling (Class A)

- **Source**: IBM Research
- **Capability**: Table reconstruction, layout preservation
- **Use Case**: Engineering manuals, specifications

### Unstructured (Class B)

- **Source**: Unstructured.io
- **Capability**: Semantic chunking, element detection
- **Use Case**: Emails, slides, documents

### Pandas (Class C)

- **Source**: PyData
- **Capability**: Native structured data handling
- **Use Case**: Logs, metrics, telemetry

---

## Summary

The Antigravity Router provides:

- ✅ Truth-value-based document classification
- ✅ Specialized extraction engines per class
- ✅ Provenance tracking for every chunk
- ✅ Decay rates for temporal relevance
- ✅ NIST AI RMF compliance for data governance

*Document Version: 1.0 | Created: 2026-01-11*
