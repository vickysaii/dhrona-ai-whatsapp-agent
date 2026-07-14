from typing import List, Dict
from app.services.memory import MemoryManager


class PromptBuilder:

    @staticmethod
    def build(
        business: Dict,
        system_prompt: str,
        knowledge_chunks: List[Dict],
        conversation_history: List[Dict],
        customer_message: str,
    ) -> str:
        """
        Builds the complete prompt for the LLM.
        """

        # -----------------------
        # Business Context
        # -----------------------
        business_context = f"""
Business Name:
{business.get("business_name", "")}

Business Description:
{business.get("business_description", "")}
"""

        # -----------------------
        # Knowledge Base
        # -----------------------
        knowledge_context = "\n\n".join(
            chunk["content"] for chunk in knowledge_chunks
        )

        if not knowledge_context:
            knowledge_context = "No relevant knowledge found."

        # -----------------------
        # Conversation History
        # -----------------------
        history = ""

        for message in conversation_history:

            role = "Customer"

            if message["sender"] == "agent":
                role = "Assistant"

            history += f"{role}: {message['content']}\n"

        if not history:
            history = "No previous conversation."

        # -----------------------
        # Customer Memory
        # -----------------------
        customer_memory = MemoryManager.extract_customer_memory(
            conversation_history
        )

        # -----------------------
        # Final Prompt
        # -----------------------
        prompt = f"""
{system_prompt}

You are an AI assistant for this business.

IMPORTANT RULES:

1. This is an ongoing conversation.
2. Use the CUSTOMER MEMORY first.
3. Use the PREVIOUS CONVERSATION to maintain context.
4. Use the KNOWLEDGE BASE to answer business-related questions.
5. Never ask the customer to repeat information already available.
6. Resolve references like "it", "they", "them", "my", "that", etc.
7. If the answer exists in CUSTOMER MEMORY, use it.
8. If the answer exists in the KNOWLEDGE BASE, use it.
9. If neither contains the answer, politely say you don't know.

==================================================
BUSINESS INFORMATION
==================================================

{business_context}

==================================================
CUSTOMER MEMORY
==================================================

{customer_memory}

==================================================
KNOWLEDGE BASE
==================================================

{knowledge_context}

==================================================
PREVIOUS CONVERSATION
==================================================

{history}

==================================================
CURRENT CUSTOMER MESSAGE
==================================================

{customer_message}

Answer naturally as if you are continuing the same conversation.
"""

        print("\n" + "=" * 80)
        print("FINAL PROMPT")
        print("=" * 80)
        print(prompt)
        print("=" * 80 + "\n")

        return prompt