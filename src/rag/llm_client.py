"""
LLMClient Module

Responsible for communicating with the Mistral AI API.
Isolates all Mistral-specific LLM invocation and error handling.
"""

import logging
import os
from typing import Any, Optional

from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMClient:
    """
    LLMClient isolates interactions with the Mistral AI API.
    
    Responsible for sending prompts, returning text responses, 
    validating inputs, and handling API errors.
    """

    def __init__(self, llm: Optional[Any] = None, model_name: str = "mistral-large-latest", temperature: float = 0.2):
        """
        Initialize the LLMClient with ChatMistralAI.

        Args:
            llm (Optional[Any]): Custom LLM instance for testing or dependency injection.
            model_name (str): Mistral AI model name. Defaults to 'mistral-large-latest'.
            temperature (float): Model sampling temperature. Defaults to 0.2.

        Raises:
            ValueError: If MISTRAL_API_KEY environment variable is not set or empty.
            RuntimeError: If client initialization fails.
        """
        if llm is not None:
            self.llm = llm
            logger.info("LLMClient initialized with custom LLM instance.")
            return

        load_dotenv()
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY environment variable is not set or empty.")

        try:
            self.llm = ChatMistralAI(
                model=model_name,
                temperature=temperature,
                api_key=api_key
            )
            logger.info(f"LLMClient initialized successfully with model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Mistral LLM client: {e}")
            raise RuntimeError(f"Initialization error: {e}")
    @staticmethod
    def _validate_prompt(prompt) -> str:
        """
        Validate that the input prompt is a non-empty string.

        Args:
            prompt : Prompt string to validate.

        Returns:
            str: Stripped prompt string.

        Raises:
            ValueError: If prompt is None, non-string, or empty/whitespace-only.
        """
        if prompt is None:
            raise ValueError("Prompt cannot be None.")
        if not isinstance(prompt, str):
            raise ValueError("Prompt must be a string.")
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")
        return prompt.strip()

    def generate(self, prompt: str) -> str:
        """
        Send a prompt to the Mistral AI model and return the generated text response.

        Args:
            prompt (str): The prompt string to send to the LLM.

        Returns:
            str: Generated text response from the model.

        Raises:
            ValueError: If prompt is invalid.
            RuntimeError: If Mistral API call fails.
        """
        cleaned_prompt = self._validate_prompt(prompt)
        logger.info("Sending prompt to Mistral AI API.")

        try:
            response = self.llm.invoke(cleaned_prompt)
            if hasattr(response, "content"):
                text = str(response.content)
            else:
                text = str(response)
            logger.info("Successfully received response from Mistral AI API.")
            return text
        except Exception as e:
            logger.error(f"Mistral API generation error: {e}")
            raise RuntimeError(f"Mistral API generation failed: {e}")

    def health_check(self) -> bool:
        """
        Check if the client is initialized correctly.

        Returns:
            bool: True if the client is initialized correctly, False otherwise.
        """
        return self.llm is not None
