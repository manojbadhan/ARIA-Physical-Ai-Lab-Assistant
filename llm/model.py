from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL
from groq import APIConnectionError, APITimeoutError, RateLimitError
from llm.prompts import SYSTEM_PROMPT , RAG_SYSTEM_PROMPT
class LabAssistantLLM:

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = GROQ_MODEL

    def generate_response(
        self,
        user_message,
        system_prompt,
        conversation_history=None,
        retrieved_context=None,
        max_history_turns=8,
    ):
        messages = [{"role": "system", "content": system_prompt}]

        # cap history so payload doesn't grow unbounded over a long session
        if conversation_history:
            messages.extend(conversation_history[-max_history_turns:])

        # if RAG found relevant notes, ground the question in them
        if retrieved_context:
            user_message = (
                f"Relevant notes:\n{retrieved_context}\n\n"
                f"Question: {user_message}\n\n"
                "Answer using only the notes above. If the notes don't "
                "cover this, say clearly that you don't have information "
                "on it — do not guess."
            )

        messages.append({"role": "user", "content": user_message})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,   # lower = more grounded, less improvised
                max_tokens=1000,
                timeout=30,
            )
            return response.choices[0].message.content

        # Groq's SDK raises various exception types (APIConnectionError,
        # APITimeoutError, RateLimitError, etc.) — catching broadly here
        # keeps the assistant from crashing mid-demo; log the real error
        # for debugging instead of hiding it entirely.
        except APIConnectionError:
            return "I couldn't connect to the model service. Check your internet connection."
        except APITimeoutError:
            return "The model took too long to respond. Please try again."
        except RateLimitError:
            return "I'm being rate-limited right now — please wait a moment and try again."
        except Exception as error:
            print(f"[LLM ERROR] {error}")
            return "Something went wrong generating a response."

if __name__ == "__main__":
    llm = LabAssistantLLM()

    response = llm.generate_response(
        user_message="what is a 3d printer?",
        system_prompt=SYSTEM_PROMPT
    )

    print("\nAssistant:", response)