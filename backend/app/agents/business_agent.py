import time
from typing import Dict, Any

from app.repositories.db_repo import DatabaseRepository
from app.services.llm.groq import LLMService
from app.services.embeddings.fastembed import EmbeddingService
from app.services.prompt import PromptBuilder
from app.services.whatsapp.service import WhatsAppService

# Initialize services once
llm = LLMService()
embedder = EmbeddingService()


class BusinessAgent:

    @staticmethod
    def process_message(
        customer_phone: str,
        customer_message: str,
        customer_name: str = None,
    ) -> Dict[str, Any]:

        start_time = time.time()

        # -----------------------------
        # STEP 1: Get/Create Session
        # -----------------------------
        session = DatabaseRepository.get_or_create_session(
            customer_phone,
            customer_name
        )

        session_id = session["id"]

        # -----------------------------
        # STEP 2: Save Customer Message
        # -----------------------------
        DatabaseRepository.create_message(
            session_id=session_id,
            sender="customer",
            message_type="text",
            content=customer_message
        )

        # -----------------------------
        # STEP 3: Generate Query Embedding
        # -----------------------------
        query_embedding = embedder.embed_query(customer_message)

        # -----------------------------
        # STEP 4: Retrieve Knowledge
        # -----------------------------
        knowledge = DatabaseRepository.match_knowledge_chunks(
            query_embedding=query_embedding,
            match_threshold=0.50,
            match_count=5
        )

        # -----------------------------
        # STEP 5: Load Business Settings
        # -----------------------------
        business = DatabaseRepository.get_business_settings()

        prompt_settings = DatabaseRepository.get_prompt_settings()

        # -----------------------------
        # STEP 6: Load Conversation History
        # -----------------------------
        conversation_history = DatabaseRepository.get_recent_messages(
            session_id=session_id,
            limit=10
        )

        # -----------------------------
        # STEP 7: Build Prompt
        # -----------------------------
        prompt = PromptBuilder.build(
            business=business,
            system_prompt=prompt_settings["system_prompt"],
            knowledge_chunks=knowledge,
            conversation_history=conversation_history,
            customer_message=customer_message,
        )

        # -----------------------------
        # STEP 8: Generate AI Response
        # -----------------------------
        answer, tokens = llm.generate_chat_response(
            prompt=prompt,
            system_instruction=prompt_settings["system_prompt"],
            temperature=prompt_settings["llm_temperature"],
            max_tokens=prompt_settings["max_tokens"]
        )

        # -----------------------------
        # STEP 9: Save AI Message
        # -----------------------------
        DatabaseRepository.create_message(
            session_id=session_id,
            sender="agent",
            message_type="text",
            content=answer
        )

        # -----------------------------
        # STEP 10: Save Conversation Log
        # -----------------------------
        elapsed = int((time.time() - start_time) * 1000)

        DatabaseRepository.create_conversation_log(
            session_id=session_id,
            input_text=customer_message,
            retrieved_chunks=[
                chunk["content"] for chunk in knowledge
            ],
            output_text=answer,
            tokens_used=tokens,
            response_time_ms=elapsed
        )

        # -----------------------------
        # STEP 11: Collect Source Documents
        # -----------------------------
        sources = []

        seen = set()

        for chunk in knowledge:

            metadata = chunk.get("metadata", {})

            source = metadata.get("source")

            if not source or source in seen:
                continue

            seen.add(source)

            sources.append({
                "document": source,
                "similarity": round(chunk.get("similarity", 0), 3)
            })

        # -----------------------------
        # STEP 12: Return Response
        # -----------------------------
        return {
            "reply": answer,
            "session_id": session_id,
            "knowledge_chunks": len(knowledge),
            "sources": sources,
            "tokens_used": tokens,
            "response_time_ms": elapsed
        }

    @staticmethod
    async def process_incoming_message(
        customer_phone: str,
        customer_name: str,
        customer_message: str,
        message_id: str,
    ):
        """
        Called by the WhatsApp webhook.
        Uses the existing AI pipeline and sends the reply back to WhatsApp.
        """

        try:

            print("=" * 60)
            print("Incoming WhatsApp Message")
            print(f"Phone      : {customer_phone}")
            print(f"Customer   : {customer_name}")
            print(f"Message ID : {message_id}")
            print(f"Message    : {customer_message}")
            print("=" * 60)

            # Reuse existing AI pipeline
            result = BusinessAgent.process_message(
                customer_phone=customer_phone,
                customer_message=customer_message,
                customer_name=customer_name,
            )

            reply = result["reply"]

            print("\nAI Response:")
            print(reply)

            # Send WhatsApp reply
            response = await WhatsAppService.send_text_message(
                phone_number=customer_phone,
                message=reply,
            )

            print("\nWhatsApp Response:")
            print(response)

            print("✅ Reply successfully sent.")

        except Exception as e:
            print(f"❌ BusinessAgent Error: {e}")