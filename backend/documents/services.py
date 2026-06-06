import PyPDF2
from transformers import pipeline
from datetime import datetime

class RealAISummarizer:
    """Uses REAL AI to summarize legal documents"""
    
    def __init__(self):
        print("Loading AI model (this takes a minute)...")
        # This is the same type of model ChatGPT uses
        self.summarizer = pipeline("summarization", 
                                  model="facebook/bart-large-cnn")
        print("✓ AI Model ready!")
    
    def extract_text_from_pdf(self, pdf_path):
        """Get text from PDF"""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + " "
            return text.strip()
    
    def generate_real_summary(self, text):
        """Let AI do the actual work"""
        # AI will read and understand the document
        result = self.summarizer(text[:2000],  # First 2000 chars
                                max_length=300,
                                min_length=100)
        return result[0]['summary_text']
    
    def process_document(self, document):
        """Process with REAL AI"""
        try:
            text = self.extract_text_from_pdf(document.file.path)
            
            # Let AI generate the summary - NO RULES, just understanding
            ai_summary = self.generate_real_summary(text)
            
            document.summary = ai_summary
            document.is_processed = True
            document.processed_at = datetime.now()
            document.save()
            
            print("✓ REAL AI Summary generated!")
            return True
            
        except Exception as e:
            print(f"Error: {e}")
            return False