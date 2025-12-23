"""
Translation module for the French-Wolof Translator.
Provides the main translation interface for end users.
"""
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from typing import Optional
from config import ModelConfig, DatasetConfig


class FrenchWolofTranslator:
    """Main translator class for French-Wolof translation."""
    
    # NLLB language codes (BCP-47 format)
    LANGUAGE_CODES = {
        "fr": "fra_Latn",  # French (Latin script)
        "wo": "wol_Latn",  # Wolof (Latin script)
    }
    
    def __init__(
        self,
        model_checkpoint: str,
        device: Optional[str] = None,
        model_config: Optional[ModelConfig] = None,
        dataset_config: Optional[DatasetConfig] = None
    ):
        """
        Initialize the translator.
        
        Args:
            model_checkpoint: HuggingFace model checkpoint path
            device: Device to run inference on ('cuda', 'cpu', or None for auto)
            model_config: Optional model configuration
            dataset_config: Optional dataset configuration
        """
        self.model_checkpoint = model_checkpoint
        self.model_config = model_config or ModelConfig()
        self.dataset_config = dataset_config or DatasetConfig()
        
        # Setup device
        if device is None:
            self.device = torch.device(
                "cuda" if torch.cuda.is_available() else "cpu"
            )
        else:
            self.device = torch.device(device)
        
        # Load tokenizer and model
        # NLLB models require language codes to be set
        self.tokenizer = AutoTokenizer.from_pretrained(model_checkpoint, src_lang="fra_Latn")
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_checkpoint)
        self.model.to(self.device)
        self.model.eval()
        
        # Cache language token IDs for faster translation
        self._lang_token_ids = {}
        for lang_code, bcp47_code in self.LANGUAGE_CODES.items():
            self._lang_token_ids[lang_code] = self.tokenizer.convert_tokens_to_ids(bcp47_code)
    
    def translate(
        self,
        text: str,
        source_lang: str = "fr",
        max_length: Optional[int] = None
    ) -> str:
        """
        Translate text from French to Wolof or Wolof to French.
        
        Args:
            text: Text to translate
            source_lang: Source language code ('fr' for French, 'wo' for Wolof)
            max_length: Maximum generation length (uses config default if None)
            
        Returns:
            Translated text
            
        Raises:
            ValueError: If source_lang is not 'fr' or 'wo'
        """
        source_lang = source_lang.lower()
        
        if source_lang not in self.LANGUAGE_CODES:
            raise ValueError(
                f"Invalid language code: {source_lang}. "
                "Use 'fr' for French or 'wo' for Wolof."
            )
        
        # Determine target language
        target_lang = "wo" if source_lang == "fr" else "fr"
        
        # Get language codes
        src_bcp47 = self.LANGUAGE_CODES[source_lang]
        tgt_bcp47 = self.LANGUAGE_CODES[target_lang]
        
        # Set source language in tokenizer
        self.tokenizer.src_lang = src_bcp47
        
        # Prepare input
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=self.model_config.max_length
        ).to(self.device)
        
        # Get target language token ID for forced BOS token
        forced_bos_token_id = self.tokenizer.convert_tokens_to_ids(tgt_bcp47)
        
        # Generate translation
        max_gen_length = (
            max_length or self.model_config.max_generation_length
        )
        translated_tokens = self.model.generate(
            **inputs,
            forced_bos_token_id=forced_bos_token_id,
            max_length=max_gen_length,
            num_beams=5,
            early_stopping=True
        )
        
        # Decode and return (skip the language token)
        translated_text = self.tokenizer.batch_decode(
            translated_tokens,
            skip_special_tokens=True
        )[0]
        
        return translated_text
    
    def translate_french_to_wolof(self, text: str) -> str:
        """
        Convenience method to translate French to Wolof.
        
        Args:
            text: French text to translate
            
        Returns:
            Translated Wolof text
        """
        return self.translate(text, source_lang="fr")
    
    def translate_wolof_to_french(self, text: str) -> str:
        """
        Convenience method to translate Wolof to French.
        
        Args:
            text: Wolof text to translate
            
        Returns:
            Translated French text
        """
        return self.translate(text, source_lang="wo")
    
    def push_to_hub(
        self,
        hub_model_id: str,
        token: Optional[str] = None
    ):
        """
        Push the model and tokenizer to HuggingFace Hub.
        
        Args:
            hub_model_id: Model ID on HuggingFace Hub
            token: HuggingFace authentication token
        """
        self.model.push_to_hub(hub_model_id, token=token)
        self.tokenizer.push_to_hub(hub_model_id, token=token)

