"""
RAG Pipeline Module

Responsible for generating AI answers using the Retriever and Mistral Chat Model.
"""

import logging
import os
from typing import List, Dict, Any

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_mistralai import ChatMistralAI

from src.retrieval.retriever import Retriever

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGPipeline:
    """
    RAG Pipeline for answering questions using retrieved context and Mistral AI.
    """

    def __init__(self):
        """
        Initializes the Retriever and ChatMistralAI model.
        """
        load_dotenv()
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY environment variable is not set or empty.")
            
        try:
            self.retriever = Retriever()
            
            # Initialize the Mistral Chat model
            self.llm = ChatMistralAI(
                model="mistral-large-latest",
                temperature=0.2,
                api_key=api_key
            )
            logger.info("RAGPipeline initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize RAGPipeline: {e}")
            raise RuntimeError(f"Initialization error: {e}")

    def _create_context(self, documents: List[Document]) -> str:
        """
        Create a formatted context string from a list of retrieved documents.
        
        Args:
            documents (List[Document]): The retrieved documents.
            
        Returns:
            str: A formatted string of context.
        """
        if not documents:
            return ""
            
        separator = "\n----------------------------------------\n"
        context_parts = [doc.page_content for doc in documents]
        return separator.join(context_parts)

    def generate_answer(self, question: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Generate an answer for the given question based on retrieved context.
        
        Args:
            question (str): The user's question.
            top_k (int, optional): Number of documents to retrieve. Defaults to 5.
            
        Returns:
            Dict[str, Any]: A dictionary containing the question, answer, 
                            and retrieved documents.
                            
        Raises:
            ValueError: If the question is empty.
            RuntimeError: If document retrieval or LLM invocation fails.
        """
        # 1. Validate question
        if not question or not question.strip():
            raise ValueError("The question cannot be empty.")
            
        logger.info("Question received")

        # 2. Retrieve documents
        logger.info("Retrieving context")
        try:
            documents = self.retriever.search(question, top_k=top_k)
        except Exception as e:
            logger.error(f"Retriever failure: {e}")
            raise RuntimeError(f"Failed to retrieve documents: {e}")

        # 3. Create context
        context = self._create_context(documents)
        logger.info("Context built")

        # 4. Build prompt
        prompt = (
            "You are an AI Marketing Analytics Assistant.\n"
            "Answer the user's question using ONLY the provided context.\n"
            "If the answer cannot be found in the context, \n"
            "reply that the information is unavailable.\n\n"
            "Context\n"
            f"{context}\n\n"
            "Question\n"
            f"{question}\n\n"
            "Answer\n"
        )

        # 5. Invoke ChatMistralAI
        logger.info("Calling Mistral")
        try:
            response = self.llm.invoke(prompt)
            answer_text = response.content if hasattr(response, 'content') else str(response)
            logger.info("Answer generated")
        except Exception as e:
            logger.error(f"Mistral API failure: {e}")
            raise RuntimeError(f"Failed to generate answer from Mistral: {e}")

        # 6. Return a dictionary
        return {
            "question": question,
            "answer": answer_text,
            "context_documents": documents,
            "retrieved_documents": len(documents)
        }
