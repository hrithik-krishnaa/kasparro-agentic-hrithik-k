def generate_competitor_profile(product_name: str):
    """
    Deterministic logic to create a fictional competitor.
    Satisfies Requirement: Product B must be fictional but structured.
    """
    return {
        "name": f"Generic {product_name.split()[-1]} B",
        "price": "₹1200", 
        "ingredients": ["Water", "Alcohol", "Trace Active Ingredients"],
        "benefits": ["Basic Hydration"]
    }

def validate_faq_count(faqs: list) -> bool:
    """
    Strictly enforce the 15+ FAQ rule.
    """
    return len(faqs) >= 15