import json
import os
from src.models import ProductData
from src.agents import FAQAgent, ComparisonAgent
from src.logic_blocks import generate_competitor_profile, validate_faq_count

class ContentOrchestrator:
    def __init__(self):
        self.faq_agent = FAQAgent()
        self.comp_agent = ComparisonAgent()
        os.makedirs("output", exist_ok=True)

    def run_pipeline(self, input_file: str):
        print("--- Starting Agentic Pipeline ---")
        
        # 1. Load Data
        with open(input_file, 'r') as f:
            data = json.load(f)
        product = ProductData(**data)
        print(f"   [System] Loaded: {product.product_name}")

        # 2. Run FAQ Agent
        faq_page = self.faq_agent.generate(product.model_dump())
        
        # 3. Validate Count
        if validate_faq_count(faq_page.faqs):
            print(f"   [Validation] Success: {len(faq_page.faqs)} FAQs generated.")
        else:
            print(f"   [Validation] Warning: Only {len(faq_page.faqs)} FAQs. (Retry recommended)")
            
        self._save("faq.json", faq_page.model_dump())

        # 4. Run Comparison Agent
        comp_profile = generate_competitor_profile(product.product_name) # Logic Block
        comp_page = self.comp_agent.generate(product.model_dump(), comp_profile)
        self._save("comparison_page.json", comp_page.model_dump())

        # 5. Generate Product Page (Template)
        prod_page = {
            "title": product.product_name,
            "specs": product.model_dump(),
            "marketing_slug": f"The best {product.concentration} solution for {product.skin_type} skin."
        }
        self._save("product_page.json", prod_page)
        print("--- Pipeline Complete ---")

    def _save(self, filename, data):
        with open(f"output/{filename}", "w") as f:
            json.dump(data, f, indent=4)
        print(f"   [System] Saved output/{filename}")