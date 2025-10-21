python
import os
import json
from google import genai
from dotenv import load_dotenv

# .env ഫയലിൽ നിന്ന് API Key ലോഡ് ചെയ്യുന്നു
load_dotenv()

# API Key ഉപയോഗിച്ച് Gemini ക്ലയിന്റിനെ ഉണ്ടാക്കുന്നു
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

# AI ഏജന്റിന്റെ നിർദ്ദേശം (System Prompt)
SYSTEM_PROMPT = """
നിങ്ങളൊരു വിദഗ്ദ്ധനായ 'ഫീൽഡ് സെയിൽസ് ഏജന്റ് അസിസ്റ്റന്റ്' ആണ്. 
ഉപയോക്താവ് (സെയിൽസ് ഏജന്റ്) പറയുന്ന വോയിസ് ഓർഡറുകൾ കൃത്യമായി JSON 
ഫോർമാറ്റിൽ ആക്കുകയാണ് നിങ്ങളുടെ ജോലി. 
ഓർഡറിൽ ഉൾപ്പെടുന്നവ, അളവുകൾ, യൂണിറ്റുകൾ എന്നിവ ഉൾപ്പെടുത്തണം.

നിങ്ങളുടെ ഔട്ട്പുട്ട് എപ്പോഴും ഒരു ഒറ്റ JSON ഒബ്ജക്ട് മാത്രമായിരിക്കണം.
JSON ഫോർമാറ്റ്:
{
  "customer_name": "ഉപയോക്താവിന്റെ പേര്",
  "order_date": "YYYY-MM-DD",
  "order_type": "Sales Order",
  "items": [
    {
      "product_name": "ഉൽപ്പന്നത്തിന്റെ പേര്", 
      "quantity": 10, 
      "unit": "kg"
    },
    {
      "product_name": "ചായപ്പൊടി", 
      "quantity": 5, 
      "unit": "packet"
    }
  ]
}
"""

def generate_order_json(voice_input):
    """വോയിസ് ഇൻപുട്ട് ഉപയോഗിച്ച് ഓർഡർ JSON ഉണ്ടാക്കുന്നു."""
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=voice_input,
        config={
            "system_instruction": SYSTEM_PROMPT,
            "response_mime_type": "application/json", # JSON ഔട്ട്പുട്ട് ഉറപ്പാക്കുന്നു
        }
    )
    return response.text

# പരീക്ഷിക്കാനായി ഒരു ഇൻപുട്ട് നൽകുന്നു
voice_order = "ജോൺസ് ബേക്കറിക്ക് 15 കിലോ മൈദയും, 20 ലിറ്റർ പാക്കറ്റ് പാലും വേണം. ഡെലിവറി നാളെ."

# നിലവിലെ തീയതി ഓട്ടോമാറ്റിക്കായി ചേർക്കുന്നതിനുള്ള കോഡ് (ലളിതമാക്കാൻ ഒഴിവാക്കുന്നു)
# തീയതി AI തന്നെ നൽകും.

print(f"വോയിസ് ഇൻപുട്ട്: {voice_order}")
order_json = generate_order_json(voice_order)
print("\nAI ഉണ്ടാക്കിയ ഓർഡർ (JSON):")
print(order_json)

