from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from config import Config

class TextSummarizer:
    def __init__(self):
        self.config = Config()
        self.device = 0 if torch.cuda.is_available() else -1
        
        # Load model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.SUMMARIZATION_MODEL)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.config.SUMMARIZATION_MODEL)
        
        # Create summarization pipeline
        self.summarizer = pipeline(
            "summarization",
            model=self.model,
            tokenizer=self.tokenizer,
            device=self.device
        )
    
    def summarize(self, text, max_length=None, min_length=None):
        """Generate summary of text"""
        if not text or len(text.split()) < 50:
            return text
        
        if max_length is None:
            max_length = self.config.MAX_SUMMARY_LENGTH
        if min_length is None:
            min_length = self.config.MIN_SUMMARY_LENGTH
        
        try:
            # Tokenize to check length
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=1024)
            
            # Generate summary
            summary = self.summarizer(
                text,
                max_length=max_length,
                min_length=min_length,
                num_beams=self.config.NUM_BEAMS,
                length_penalty=2.0,
                early_stopping=True,
                no_repeat_ngram_size=3
            )
            
            return summary[0]['summary_text']
        except Exception as e:
            print(f"Error in summarization: {e}")
            # Fallback: return first few sentences
            sentences = text.split('. ')
            return '. '.join(sentences[:3]) + '.'
    
    def summarize_batch(self, texts, max_length=None, min_length=None):
        """Summarize multiple texts"""
        return [self.summarize(text, max_length, min_length) for text in texts]