from typing import Optional, List
from nemoguardrails.actions import action

@action()
async def self_check_input(
    context: Optional[dict] = None,
) -> bool:
    """Custom implementation for self_check_input to verify policy compliance.
    
    Returns True if the message is allowed, False if it should be blocked.
    """
    # Get the user message from the context
    user_input = context.get('user_message', '')
    print(f"Checking input: '{user_input}'")
    

    if user_input and ("system prompt" in user_input.lower() or "instructions" in user_input.lower()):
        print("Message blocked: Contains reference to system prompt or instructions")
        return False
        
    # Default to allowing the message
    print("Message allowed by default")
    return True 