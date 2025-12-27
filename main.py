from dotenv import load_dotenv
from src.orchestrator import ContentOrchestrator

load_dotenv()

if __name__ == "__main__":
    system = ContentOrchestrator()
    system.run_pipeline("data/input_product.json")