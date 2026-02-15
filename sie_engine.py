# sie_engine.py
"""
SIE Engine v4.0 - Structured Information Extraction
Entry point for the Arkhe(n) OS Cognitive Engine.
"""

import asyncio
from arkhe import DocumentProcessor, SchemaValidator, TelemetryCollector

async def run_extraction(text: str, doc_id: str, gemini_key: str = None):
    # Initialize processor
    processor = DocumentProcessor(gemini_key=gemini_key)

    # Process document
    result = await processor.process_document(text, doc_id)

    # Display Telemetry
    print(f"Extraction complete for {doc_id}")
    print(f"Reconciled Confidence: {result.reconciled_state.get('confidence', 0):.2f}")
    print(f"Metrics: {result.metrics}")

    return result

if __name__ == "__main__":
    sample_text = "Arkhe(n) OS implements a toroidal hypergraph for universal coherence."
    asyncio.run(run_extraction(sample_text, "sample_001"))
