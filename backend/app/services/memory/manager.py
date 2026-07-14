from typing import List, Dict


class MemoryManager:
    """
    Extracts important customer facts from the conversation.
    """

    @staticmethod
    def extract_customer_memory(messages: List[Dict]) -> str:

        facts = []

        for msg in messages:

            if msg["sender"] != "customer":
                continue

            text = msg["content"].strip()

            lower = text.lower()

            if "my name is" in lower:
                facts.append(f"Name: {text}")

            elif lower.startswith("i am"):
                facts.append(f"About Customer: {text}")

            elif "i work" in lower:
                facts.append(f"Work: {text}")

            elif "i live" in lower:
                facts.append(f"Location: {text}")

            elif "my company" in lower:
                facts.append(f"Company: {text}")

            elif "my email" in lower:
                facts.append(f"Email: {text}")

            elif "my phone" in lower:
                facts.append(f"Phone: {text}")

            elif "i like" in lower:
                facts.append(f"Preference: {text}")

        if not facts:
            return "No customer memory available."

        # Remove duplicates while preserving order
        unique = list(dict.fromkeys(facts))

        return "\n".join(unique)