from nemoguardrails import LLMRails, RailsConfig
from pathlib import Path


class GuardrailException(Exception):
    pass

class Guardrail():
    def __init__(self):
        # Get current file path and parent directory
        current_file = Path(__file__)
        parent_dir = current_file.parent.parent.absolute()
        print(f"Current file path: {current_file}")
        print(f"Parent directory absolute path: {parent_dir}")
        self.config = RailsConfig.from_path(str(parent_dir / "config"))
        self.rails = LLMRails(self.config)

    async def run(self, user_input: str) -> str:
        print(f"Running guardrail for user input: {user_input}")
        guardrail_response = await self.rails.generate_async(messages=[{"role": "user", "content": user_input}])
        # Check if request was blocked by guardrails
        if "I'm sorry, I can't respond to that" in guardrail_response.get("content", ""):
            raise GuardrailException("Request blocked by guardrails")

