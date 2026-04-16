# CURRENT: Single LLM (Ollama Cloud)
# FUTURE: Replace with AI Router that selects domain-specific expert models:
# - marketing_planner
# - finance_planner
# - operations_planner

# WARNING: Prompt is tightly coupled to current marketing MVP use case.
# This will need abstraction when adding multi-domain planning support.

from typing import Any, Generator
from ollama import Client


class PlannerLLM:
    def __init__(self, generate_prompt: str, refine_prompt: str, structure_prompt: str, api_key: str, model: str='gpt-oss:120b-cloud') -> None:
        self.model = model
        self.generate_prompt = generate_prompt
        self.refine_prompt = refine_prompt
        self.structure_prompt = structure_prompt

        # EXTENSION POINT:
        # Must change this code depending on the LLM you are using.
        # The methods later on must also be changed accordingly
        self.client = Client(
            host='https://ollama.com',
            headers={'Authorization': f"Bearer {api_key}"}
        )

    def __stream_prompt(self, prompt: str):  # Stream return
        stream = self.client.chat(
            model=self.model,
            messages=[{'role': 'user', 'content': prompt}],
            stream=True
        )
        return stream

    def generate_plan(self, data: str) -> Generator[str, Any, None]:
        prompt = self.generate_prompt.format(initial_data=data)
        stream = self.__stream_prompt(prompt)
        full_response = ""
        for chunk in stream:
            token = chunk["message"]["content"]
            full_response += token
            yield full_response

    def refine_plan(self, plan: str, feedback: str) -> Generator[str, Any, None]:
        prompt = self.refine_prompt.format(curr_plan=plan, feedback=feedback)
        stream = self.__stream_prompt(prompt)
        full_response = ""
        for chunk in stream:
            token = chunk["message"]["content"]
            full_response += token
            yield full_response

    def structure_data(self, plan: str) -> Generator[str, Any, None]:
        prompt = self.structure_prompt.format(generator_output=plan)
        stream = self.__stream_prompt(prompt)
        full_response = ""
        for chunk in stream:
            token = chunk["message"]["content"]
            full_response += token
            yield full_response
