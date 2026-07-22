"""
PromptBuilder Module

Responsible for formatting LLM prompts for the RAG pipeline.
Converts user questions and retrieved documents into a structured prompt.
"""

from typing import Any, List


class PromptBuilder:
    """
    PromptBuilder constructs structured prompts for LLM invocation.

    It purely formats context and prompts without performing retrieval,
    calling LLMs, modifying documents, or summarizing text.
    """

    def _validate_question(self, question: Any) -> str:
        """Validate that question is a non-empty string."""
        if question is None:
            raise ValueError("question cannot be None.")
        if not isinstance(question, str):
            raise ValueError("question must be a string.")
        if not question.strip():
            raise ValueError("question cannot be empty.")
        return question.strip()

    def _validate_documents(self, documents: Any) -> None:
        """Validate that documents is a list."""
        if documents is None:
            raise ValueError("documents cannot be None.")
        if not isinstance(documents, list):
            raise ValueError("documents must be a list.")

    def build_context(self, documents: List[Any]) -> str:
        """
        Build a formatted context string from retrieved documents.

        Args:
            documents (List[Any]): List of Document objects or dicts.

        Returns:
            str: Formatted context string.

        Raises:
            ValueError: If documents is None or not a list.
        """
        self._validate_documents(documents)

        if not documents:
            return "No relevant documents found."

        context_blocks = []
        for i, doc in enumerate(documents, start=1):
            if hasattr(doc, "page_content"):
                content = doc.page_content
                metadata = getattr(doc, "metadata", {})
            elif isinstance(doc, dict):
                content = doc.get("page_content", doc.get("text", doc.get("content", "")))
                metadata = doc.get("metadata", {})
            elif isinstance(doc, str):
                content = doc
                metadata = {}
            else:
                content = str(doc)
                metadata = {}

            block_lines = [f"[Document {i}]"]
            if content:
                block_lines.append(f"Content: {content}")
            if metadata and isinstance(metadata, dict):
                meta_items = [f"{k}: {v}" for k, v in metadata.items() if k != "text"]
                if meta_items:
                    block_lines.append(f"Metadata: {', '.join(meta_items)}")

            context_blocks.append("\n".join(block_lines))

        return "\n\n".join(context_blocks)

    def build_rag_prompt(self, question: str, documents: List[Any]) -> str:
        """
        Build a complete RAG prompt ready for LLM invocation.

        Args:
            question (str): The user's question.
            documents (List[Any]): List of retrieved documents.

        Returns:
            str: Formatted prompt string.

        Raises:
            ValueError: If question or documents input is invalid.
        """
        cleaned_question = self._validate_question(question)
        context_str = self.build_context(documents)

        prompt = (
            "You are MarketMind AI.\n\n"
            "You are an intelligent marketing analytics assistant.\n\n"
            "Answer ONLY using the provided context.\n\n"
            "If the answer cannot be found in the context, respond:\n\n"
            '"I could not find this information in the available marketing reports."\n\n'
            "--------------------------------------------------\n\n"
            "Context\n\n"
            f"{context_str}\n\n"
            "--------------------------------------------------\n\n"
            "Question\n\n"
            f"{cleaned_question}\n\n"
            "--------------------------------------------------\n\n"
            "Answer"
        )
        return prompt
