import pdfplumber
from transformers import pipeline
import re
from datetime import datetime

class RealAISummarizer:
    """ChatGPT-like Legal Document Summarizer"""
    
    def __init__(self):
        print("🔄 Loading AI model (takes 2-3 mins first time)...")
        # Using BART which is excellent for summarization
        self.summarizer = pipeline("summarization", 
                                  model="facebook/bart-large-cnn")
        print("✅ AI Model Ready!")
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text properly using pdfplumber (better than PyPDF2)"""
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
        return text.strip()
    
    def split_text(self, text, chunk_size=500):
        """Split long legal documents into chunks"""
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i+chunk_size])
            chunks.append(chunk)
        return chunks
    
    def summarize_chunk(self, text_chunk):
        """Summarize a single chunk"""
        result = self.summarizer(text_chunk, 
                                max_length=150, 
                                min_length=50,
                                do_sample=False)
        return result[0]['summary_text']
    
    def generate_legal_summary(self, full_text):
        """Generate complete legal summary like ChatGPT"""
        
        # Split long document
        chunks = self.split_text(full_text)
        
        # Summarize each chunk
        chunk_summaries = []
        for chunk in chunks:
            summary = self.summarize_chunk(chunk)
            chunk_summaries.append(summary)
        
        # Combine all summaries
        combined = " ".join(chunk_summaries)
        
        # Final summary with structure
        final_prompt = f"""Summarize this legal document with the following structure:

Case Title:
Court:
Parties Involved:
Key Facts:
Legal Issues:
Evidence Presented:
Arguments:
Judgment:
Key Legal Principles:

Document: {combined[:1500]}"""

        final_summary = self.summarizer(final_prompt, 
                                       max_length=400, 
                                       min_length=200)[0]['summary_text']
        
        return final_summary
    
    def process_document(self, document):
        """Main processing function"""
        try:
            print(f"\n📄 Processing: {document.title}")
            
            # Extract text
            text = self.extract_text_from_pdf(document.file.path)
            print(f"📊 Extracted {len(text)} characters")
            
            print("🤖 AI is generating comprehensive summary...")
            
            # Generate summary
            summary = self.generate_legal_summary(text)
            
            # Save to database
            document.summary = summary
            document.is_processed = True
            document.processed_at = datetime.now()
            document.save()
            
            print("✅ Summary generated!")
            print("\n" + "="*50)
            print(summary)
            print("="*50)
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            document.processing_error = str(e)
            document.is_processed = False
            document.save()
            return False