import os
from groq import Groq

def enhance_response(raw_response: str, system_prompt: str) -> str:
    """
    Enhance Adopt's formatted response using Groq LLM to make it more conversational
    
    Args:
        raw_response: The formatted response from response_formatter
        system_prompt: Custom system prompt for context
    
    Returns:
        Enhanced, conversational response
    """
    
    # Check if Groq API key is available
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        return f"⚠️ **LLM Enhancement unavailable** (GROQ_API_KEY not set)\n\n{raw_response}"
    
    try:
        client = Groq(api_key=groq_api_key)
        
        enhancement_prompt = f"""
{system_prompt}

You received this formatted response from the Adopt platform:

{raw_response}

Please rewrite this response to be more conversational and user-friendly:
1. Make it sound natural and helpful
2. Keep all the important information
3. Use emojis strategically (but don't overdo it)
4. If it's a list of actions, explain what they're for
5. End with a helpful question or suggestion
6. Keep it concise but warm

DO NOT add any preamble like "Here's the formatted response" - just provide the enhanced content directly.
"""
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that makes technical responses warm and conversational while keeping all important details."
                },
                {
                    "role": "user",
                    "content": enhancement_prompt
                }
            ],
            temperature=0.7,  # Slightly creative
            max_tokens=1024
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        # If enhancement fails, return original formatted response
        return f"⚠️ **Enhancement failed**: {str(e)}\n\n{raw_response}"