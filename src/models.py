from typing import List, Optional
from pydantic import BaseModel

class ProductData(BaseModel):
    product_name: str
    concentration: Optional[str] = None
    skin_type: str
    key_ingredients: List[str]
    benefits: List[str]
    how_to_use: str
    side_effects: str
    price: str

class FAQItem(BaseModel):
    category: str
    question: str
    answer: str

class FAQPage(BaseModel):
    page_title: str
    faqs: List[FAQItem]

class ComparisonItem(BaseModel):
    feature: str
    glowboost_value: str
    competitor_value: str

class ComparisonPage(BaseModel):
    title: str
    product_a: str
    product_b: str
    comparison_table: List[ComparisonItem]