import google.generativeai as genai

genai.configure(api_key="your-gemini-api-key")

def summarize_with_gemini(self, text):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Summarize this legal document with case title, court, parties, key facts, legal issues, evidence, arguments, and decision:\n\n{text[:4000]}"
    response = model.generate_content(prompt)
    return response.text