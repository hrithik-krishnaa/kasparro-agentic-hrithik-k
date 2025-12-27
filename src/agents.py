import json
import os
import requests
from src.models import FAQPage, ComparisonPage

class BaseAgent:
    def __init__(self):
        # SECURITY: Load key from environment variable
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Using Gemini 2.5 Flash
        self.model_name = "gemini-2.5-flash"
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"
        self.headers = {"Content-Type": "application/json"}

    def _call_llm(self, prompt_text):
        payload = {
            "contents": [{
                "parts": [{"text": prompt_text}]
            }],
            "generationConfig": {
                "response_mime_type": "application/json"
            }
        }

        try:
            response = requests.post(self.url, headers=self.headers, json=payload)
            
            if response.status_code != 200:
                print(f"   [Error] API Status: {response.status_code}")
                # Print details to help debug
                print(f"   [Error] Details: {response.text[:200]}") 
                return {}

            data = response.json()
            
            try:
                raw_text = data['candidates'][0]['content']['parts'][0]['text']
                
                # --- THE FIX: CLEANUP MARKDOWN ---
                # Gemini sometimes wraps JSON in ```json ... ```. We must remove it.
                if "```" in raw_text:
                    raw_text = raw_text.replace("```json", "").replace("```", "").strip()
                
                return json.loads(raw_text)
                
            except (KeyError, IndexError, json.JSONDecodeError) as e:
                print(f"   [Error] Parsing JSON failed: {e}")
                # Print the raw text so we can see what went wrong
                print(f"   [Debug] Raw Text was: {raw_text[:100]}...")
                return {}

        except Exception as e:
            print(f"   [Error] Connection failed: {e}")
            return {}

class FAQAgent(BaseAgent):
    def generate(self, product_data: dict):
        print(f"   [FAQ Agent] Generating 15+ Questions using {self.model_name}...")
        
        prompt = f"""
        You are an expert Content Generator.
        Task: Create a FAQ page JSON based on this product data.
        
        CRITICAL RULES:
        1. You MUST generate AT LEAST 16 distinct questions.
        2. Categories to use: Usage, Safety, Ingredients, Results, Shipping.
        3. Output strictly in this JSON schema:
        {{
            "page_title": "Frequently Asked Questions",
            "faqs": [
                {{ "category": "Safety", "question": "...", "answer": "..." }}
            ]
        }}
        
        Product Data: {json.dumps(product_data)}
        """
        
        raw_data = self._call_llm(prompt)
        if not raw_data:
            return FAQPage(page_title="Error", faqs=[])
        return FAQPage(**raw_data)

class ComparisonAgent(BaseAgent):
    def generate(self, product_a: dict, product_b: dict):
        print(f"   [Comparison Agent] Analyzing Competitor using {self.model_name}...")
        
        prompt = f"""
        You are a Sales Expert. Compare these two products.
        Task: Create a comparison table JSON showing why Product A is better.
        
        Output Schema:
        {{
            "title": "Product Comparison",
            "product_a": "{product_a.get('product_name', 'Product A')}",
            "product_b": "{product_b.get('name', 'Competitor')}",
            "comparison_table": [
                {{ "feature": "Price", "glowboost_value": "...", "competitor_value": "..." }},
                {{ "feature": "Key Ingredient", "glowboost_value": "...", "competitor_value": "..." }},
                {{ "feature": "Safety", "glowboost_value": "...", "competitor_value": "..." }}
            ]
        }}
        
        Product A: {json.dumps(product_a)}
        Product B: {json.dumps(product_b)}
        """
        
        raw_data = self._call_llm(prompt)
        if not raw_data:
            return ComparisonPage(title="Error", product_a="", product_b="", comparison_table=[])
        return ComparisonPage(**raw_data)