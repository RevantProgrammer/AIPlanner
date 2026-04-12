from ollama import Client


class PlannerLLM:
    def __init__(self, generate_prompt, refine_prompt, api_key, model='gpt-oss:120b-cloud'):
        self.model = model
        self.generate_prompt = generate_prompt
        self.refine_prompt = refine_prompt

        self.client = Client(
            host='https://ollama.com',
            headers={'Authorization': f"Bearer {api_key}"}
        )

    def generate_plan(self, data):
        prompt = self.generate_prompt.format(initial_data=data)
        stream = self.client.chat(
            model=self.model,
            messages=[{'role': 'user', 'content': prompt}],
            stream=True
        )
        full_response = ""
        for chunk in stream:
            token = chunk["message"]["content"]
            full_response += token
            yield full_response

    def refine_plan(self, plan, feedback):
        prompt = self.refine_prompt.format(curr_plan=plan, feedback=feedback)
        stream = self.client.chat(
            model=self.model,
            messages=[{'role': 'user', 'content': prompt}],
            stream=True
        )
        full_response = ""
        for chunk in stream:
            token = chunk["message"]["content"]
            full_response += token
            yield full_response
