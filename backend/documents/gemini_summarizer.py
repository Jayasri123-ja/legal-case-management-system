import PyPDF2
from google import genai
from datetime import datetime
import time
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Configure Gemini with new package
client = genai.Client(api_key="AIzaSyCFnqjIZHZaVs2lRTQYUwzIUhE41KOKRVY")

class GeminiSummarizer:
    """Uses Google's FREE Gemini AI with retry logic for reliability"""
    
    def __init__(self):
        print("✅ Connected to Google Gemini AI")
        # Try different models if one fails
        self.models_to_try = [
    "models/gemini-2.0-flash",
    "models/gemini-2.0-flash-lite", 
    "models/gemma-3-27b-it"
]
        self.current_model_index = 0
        self.model_name = self.models_to_try[0]
        print(f"📋 Using model: {self.model_name}")
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF"""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + " "
                return text.strip()
        except Exception as e:
            print(f"PDF Error: {e}")
            return None
    
    def call_gemini_api(self, prompt, max_retries=3):
        """Call Gemini API with retry logic and model fallback"""
        
        for attempt in range(max_retries):
            try:
                print(f"🔄 API attempt {attempt + 1}/{max_retries}...")
                
                response = client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                
                if response and response.text:
                    return response.text
                    
            except Exception as e:
                error_msg = str(e)
                print(f"❌ Attempt {attempt + 1} failed: {error_msg}")
                
                
                if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                    print("⚠️ Rate limit hit. Switching to next model...")
                    self.switch_to_next_model()
                    time.sleep(5)  # Wait before retry
                    continue
                    
                
                if "503" in error_msg or "UNAVAILABLE" in error_msg:
                    print("⚠️ Service unavailable. Waiting 10 seconds...")
                    time.sleep(10)
                    continue
                
               
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 5
                    print(f"⚠️ Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                    continue
                    
        return None
    
    def switch_to_next_model(self):
        """Switch to next available model when quota is exhausted"""
        self.current_model_index += 1
        if self.current_model_index < len(self.models_to_try):
            self.model_name = self.models_to_try[self.current_model_index]
            print(f"🔄 Switching to model: {self.model_name}")
        else:
            print("❌ All models exhausted. Please try again later.")
    
    def generate_legal_summary(self, text):
        """Generate structured legal summary with retry logic"""
        
        prompt = f"""
        You are a professional legal summarizer. Analyze this legal document and provide a concise, professional summary using this EXACT format:

        CASE TITLE:
        [Full case name - one line only]

        COURT:
        [Court name, case number (if any), date - one line only]

        PARTIES:
        - Complainant: [Name only, no description]
        - Accused: [Name only, no description]

        KEY FACTS:
        1. [One line fact - who, what, when, amount if any]
        2. [One line fact - what happened next]
        3. [One line fact - key action taken]
        4. [One line fact - final trigger]

        LEGAL ISSUES:
        • [One line legal question]
        • [One line legal question]

        EVIDENCE PRESENTED:
        • [Key evidence - 5-7 words]
        • [Key evidence - 5-7 words]
        • [Key evidence - 5-7 words]

        ARGUMENTS:
        - Prosecution: [One sentence summary - max 15 words]
        - Defense: [One sentence summary - max 15 words]

        DECISION:
        [One sentence - what court decided]

        SENTENCE/RELIEF:
        [One line - punishment or order, if any]

        Important Rules:
        - Keep EVERY line short and concise
        - No extra explanations or commentary
        - Only include information actually in the document
        - Use professional legal language
        - Make it easy to read in 30 seconds

        Document:
        {text[:6000]}
        """
        
        try:
            result = self.call_gemini_api(prompt)
            return result
            
        except Exception as e:
            print(f"Gemini API Error after retries: {e}")
            return None
    
    def process_document(self, document):
        """Process document with Gemini and retry logic"""
        try:
            print(f"\n📄 Processing: {document.title}")
            
           
            self.current_model_index = 0
            self.model_name = self.models_to_try[0]
            
            
            text = self.extract_text_from_pdf(document.file.path)
            if not text:
                document.processing_error = "Could not extract text"
                document.is_processed = False
                document.save()
                return False
            
            print(f"📊 Extracted {len(text)} characters")
            
            
            if len(text) > 6000:
                print("📚 Document is long, taking first part...")
                text = text[:6000]
            
            print("🤖 AI is generating professional summary...")
            
            
            summary = self.generate_legal_summary(text)
            
            if not summary:
                document.processing_error = "Failed to get summary after multiple retries"
                document.is_processed = False
                document.save()
                return False
            
            # Save to database
            document.summary = summary
            document.is_processed = True
            document.processed_at = datetime.now()
            document.save()
            
            print("✅ Summary generated successfully!")
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