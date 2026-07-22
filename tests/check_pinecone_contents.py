"""
Standalone diagnostic script to inspect Pinecone index contents and search results.
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.vectorstore.pinecone_manager import PineconeManager
from src.retrieval.retriever import Retriever


def main():
    print("========================================")
    print("PINECONE INDEX DIAGNOSTIC")
    print("========================================")

    # 1. Initialize PineconeManager & Print index statistics
    pm = PineconeManager()
    stats = pm.describe_index()

    index_name = stats.get("index_name", "Unknown")
    total_vectors = stats.get("total_vectors", 0)
    dimension = stats.get("dimension", 0)

    print(f"Index Name    : {index_name}")
    print(f"Total Vectors : {total_vectors}")
    print(f"Dimension     : {dimension}")
    print("========================================\n")

    # 2. Initialize Retriever
    retriever = Retriever()

    # 3. Define target queries
    queries = [
        "marketing",
        "sales",
        "forecast",
        "customer",
        "sentiment",
        "recommendations",
    ]

    retrieval_summary = {}

    # 4. Execute queries and print retrieved documents
    for query in queries:
        print("========================================")
        print(f"QUERY: '{query}'")
        print("========================================")

        try:
            docs = retriever.search(query, top_k=5)
            retrieved_count = len(docs)
            retrieval_summary[query] = retrieved_count
            print(f"Retrieved Documents: {retrieved_count}\n")

            if retrieved_count == 0:
                print("No matching documents found.\n")
            else:
                for i, doc in enumerate(docs, start=1):
                    content = getattr(doc, "page_content", "")
                    preview = content[:300].replace("\n", " ") if content else "N/A"
                    metadata = getattr(doc, "metadata", {})

                    print("----------------------------------------")
                    print(f"Document {i}")
                    print("Metadata:")
                    if metadata:
                        for k, v in metadata.items():
                            print(f"  - {k}: {v}")
                    else:
                        print("  (None)")
                    print(f"Content (first 300 characters):\n{preview}")
                    print("----------------------------------------")
                print()

        except Exception as e:
            print(f"Error querying '{query}': {e}\n")
            retrieval_summary[query] = 0

    # 5. Print Summary
    print("========================================")
    print("Pinecone Summary")
    print("========================================")
    print(f"Total vectors: {total_vectors}")
    print(f"Queries tested: {len(queries)}")
    print("Documents retrieved for each query:")
    for q, count in retrieval_summary.items():
        print(f"  - {q}: {count}")
    print("========================================\n")


if __name__ == "__main__":
    main()
