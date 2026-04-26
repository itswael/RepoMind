from openai import OpenAI

client = OpenAI()

def extract_tasks(chunk):
    prompt = f"""
    Extract actionable tasks from this text.

    Text:
    {chunk}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return parse_json(response)