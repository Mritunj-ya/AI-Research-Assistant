import os
import ollama
from huggingface_hub import InferenceClient


class LLMService:

    def generate_answer(self, prompt):

        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        try:

            hf_token = os.getenv("HF_TOKEN")

            if hf_token:
                client = InferenceClient(
                    model="Qwen/Qwen3-8B",
                    provider="auto",
                    api_key=hf_token
                )

                response = client.chat_completion(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt + "\n/no_think"
                        }
                    ],
                    temperature=0,
                    max_tokens=2048
                )

                answer = response.choices[0].message.content

            else:
                response = ollama.chat(
                    model="qwen3:8b",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    options={"temperature": 0}
                )

                answer = response["message"]["content"]

            if not answer or not answer.strip():
                raise RuntimeError("LLM returned an empty response.")

            return answer.strip()

        except Exception as e:
            raise RuntimeError(
                f"Failed to generate LLM response: {e}"
            ) from e