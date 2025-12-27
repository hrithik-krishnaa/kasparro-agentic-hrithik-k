import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: API Key not found in .env")
    exit()

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

print(f"Checking available models for key ending in ...{api_key[-4:]}")

try:
    response = requests.get(url)
    if response.status_code == 200:
        models = response.json().get('models', [])
        print("\nSUCCESS! Here are your available models:")
        print("-" * 40)
        found_flash = False
        for m in models:
            # We only care about models that can 'generateContent'
            if "generateContent" in m.get('supportedGenerationMethods', []):
                print(f"• {m['name']}")
                if "flash" in m['name']:
                    found_flash = True
        print("-" * 40)
        
        if not found_flash:
            print("\nWARNING: 'Flash' model not found. We might need to use 'gemini-pro'.")
            
    else:
        print(f"Error accessing API: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"Connection failed: {e}")