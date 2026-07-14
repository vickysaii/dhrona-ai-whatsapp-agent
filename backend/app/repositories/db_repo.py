from typing import List, Dict, Any, Optional
from app.database import supabase
import datetime

class DatabaseRepository:
    # --- AUTH / USERS ---
    @staticmethod
    def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        try:
            res = supabase.table("users").select("*").eq("email", email).execute()
            return res.data[0] if res.data else None
        except Exception as e:
            print(f"Error fetching user by email: {e}")
            return None

    @staticmethod
    def create_user(email: str, password_hash: str, role: str = "user") -> Optional[Dict[str, Any]]:
        try:
            data = {"email": email, "password_hash": password_hash, "role": role}
            res = supabase.table("users").insert(data).execute()
            if res.data:
                user = res.data[0]
                # If role is admin, create admin record too
                if role == "admin":
                    DatabaseRepository.create_admin(user["id"], email.split("@")[0])
                return user
            return None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    @staticmethod
    def create_admin(user_id: str, full_name: str) -> Optional[Dict[str, Any]]:
        try:
            data = {"id": user_id, "full_name": full_name}
            res = supabase.table("admins").insert(data).execute()
            return res.data[0] if res.data else None
        except Exception as e:
            print(f"Error creating admin: {e}")
            return None

    # --- BUSINESS SETTINGS ---
    @staticmethod
    def get_business_settings() -> Dict[str, Any]:
        try:
            res = supabase.table("business_settings").select("*").eq("id", "default").execute()
            if res.data:
                return res.data[0]
            # Fallback if not seeded
            default_data = {
                "id": "default",
                "business_name": "My AI Business",
                "greeting_message": "Hello! Welcome to our business.",
                "fallback_message": "I am sorry, but I do not have that information at the moment."
            }
            supabase.table("business_settings").insert(default_data).execute()
            return default_data
        except Exception as e:
            print(f"Error fetching business settings: {e}")
            return {}

    @staticmethod
    def update_business_settings(data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            data["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            res = supabase.table("business_settings").upsert(data).execute()
            return res.data[0] if res.data else {}
        except Exception as e:
            print(f"Error updating business settings: {e}")
            return {}

    # --- PROMPT SETTINGS ---
    @staticmethod
    def get_prompt_settings() -> Dict[str, Any]:
        try:
            res = supabase.table("prompt_settings").select("*").eq("id", "default").execute()
            if res.data:
                return res.data[0]
            default_data = {
                "id": "default",
                "system_prompt": "You are a professional AI assistant representing this business. Answer only using the business knowledge provided. Never hallucinate.",
                "llm_temperature": 0.3,
                "max_tokens": 800
            }
            supabase.table("prompt_settings").insert(default_data).execute()
            return default_data
        except Exception as e:
            print(f"Error fetching prompt settings: {e}")
            return {}

    @staticmethod
    def update_prompt_settings(data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            data["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            res = supabase.table("prompt_settings").upsert(data).execute()
            return res.data[0] if res.data else {}
        except Exception as e:
            print(f"Error updating prompt settings: {e}")
            return {}

    # --- KNOWLEDGE BASE / FILES ---
    @staticmethod
    def create_uploaded_file(filename: str, file_type: str, supabase_storage_path: str, file_size: int) -> Optional[Dict[str, Any]]:
        try:
            data = {
                "filename": filename,
                "file_type": file_type,
                "supabase_storage_path": supabase_storage_path,
                "file_size": file_size,
                "status": "uploaded"
            }
            res = supabase.table("uploaded_files").insert(data).execute()
            return res.data[0] if res.data else None
        except Exception as e:
            print(f"Error creating uploaded file: {e}")
            return None

    @staticmethod
    def update_file_status(file_id: str, status: str) -> bool:
        try:
            supabase.table("uploaded_files").update({"status": status}).eq("id", file_id).execute()
            return True
        except Exception as e:
            print(f"Error updating file status: {e}")
            return False

    @staticmethod
    def get_uploaded_files() -> List[Dict[str, Any]]:
        try:
            res = supabase.table("uploaded_files").select("*").order("created_at", desc=True).execute()
            return res.data if res.data else []
        except Exception as e:
            print(f"Error fetching uploaded files: {e}")
            return []

    @staticmethod
    def delete_uploaded_file(file_id: str) -> bool:
        try:
            # Table knowledge_documents references file_id ON DELETE CASCADE
            # But we must delete from storage if needed or just remove DB record
            # Let's get storage path first
            res = supabase.table("uploaded_files").select("supabase_storage_path").eq("id", file_id).execute()
            if res.data:
                path = res.data[0]["supabase_storage_path"]
                if path:
                    # Optional: delete from Supabase storage bucket
                    try:
                        # Assumes bucket is named 'knowledge_base'
                        supabase.storage.from_("knowledge_base").remove([path])
                    except Exception as storage_err:
                        print(f"Storage deletion warning: {storage_err}")
            
            supabase.table("uploaded_files").delete().eq("id", file_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False

    @staticmethod
    def add_knowledge_chunk(file_id: str, content: str, embedding: List[float], metadata: Dict[str, Any]) -> bool:
        try:
            data = {
                "file_id": file_id,
                "content": content,
                "embedding": embedding,
                "metadata": metadata
            }
            supabase.table("knowledge_documents").insert(data).execute()
            return True
        except Exception as e:
            print(f"Error adding knowledge chunk: {e}")
            return False

    @staticmethod
    def match_knowledge_chunks(query_embedding: List[float], match_threshold: float = 0.5, match_count: int = 4) -> List[Dict[str, Any]]:
        try:
            # We call the RPC function defined in database.sql
            res = supabase.rpc("match_documents", {
                "query_embedding": query_embedding,
                "match_threshold": match_threshold,
                "match_count": match_count
            }).execute()
            return res.data if res.data else []
        except Exception as e:
            print(f"Error matching knowledge chunks: {e}")
            return []

    # --- CHAT SESSIONS & MESSAGES ---
    @staticmethod
    def get_or_create_session(customer_phone: str, customer_name: Optional[str] = None) -> Dict[str, Any]:
        try:
            res = supabase.table("chat_sessions").select("*").eq("customer_phone", customer_phone).execute()
            if res.data:
                return res.data[0]
            
            data = {
                "customer_phone": customer_phone,
                "customer_name": customer_name or f"WhatsApp User ({customer_phone[-4:]})"
            }
            res = supabase.table("chat_sessions").insert(data).execute()
            return res.data[0] if res.data else {}
        except Exception as e:
            print(f"Error getting/creating session: {e}")
            return {}

    @staticmethod
    def get_chat_sessions() -> List[Dict[str, Any]]:
        try:
            res = supabase.table("chat_sessions").select("*").order("updated_at", desc=True).execute()
            return res.data if res.data else []
        except Exception as e:
            print(f"Error getting chat sessions: {e}")
            return []

    @staticmethod
    def update_session_takeover(session_id: str, human_takeover: bool) -> bool:
        try:
            supabase.table("chat_sessions").update({
                "human_takeover": human_takeover,
                "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }).eq("id", session_id).execute()
            return True
        except Exception as e:
            print(f"Error updating human takeover: {e}")
            return False

    @staticmethod
    def create_message(session_id: str, sender: str, message_type: str, content: str, meta_message_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        try:
            data = {
                "session_id": session_id,
                "sender": sender,
                "message_type": message_type,
                "content": content,
                "meta_message_id": meta_message_id
            }
            res = supabase.table("messages").insert(data).execute()
            # Also touch updated_at of the session
            supabase.table("chat_sessions").update({
                "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }).eq("id", session_id).execute()
            return res.data[0] if res.data else None
        except Exception as e:
            print(f"Error creating message: {e}")
            return None

    @staticmethod
    def get_session_messages(session_id: str) -> List[Dict[str, Any]]:
        try:
            res = supabase.table("messages").select("*").eq("session_id", session_id).order("created_at", desc=False).execute()
            return res.data if res.data else []
        except Exception as e:
            print(f"Error fetching session messages: {e}")
            return []

    # --- FAQ ---
    @staticmethod
    def get_faqs() -> List[Dict[str, Any]]:
        try:
            res = supabase.table("faq").select("*").order("created_at", desc=True).execute()
            return res.data if res.data else []
        except Exception as e:
            print(f"Error fetching FAQs: {e}")
            return []

    @staticmethod
    def create_faq(question: str, answer: str) -> Optional[Dict[str, Any]]:
        try:
            data = {"question": question, "answer": answer}
            res = supabase.table("faq").insert(data).execute()
            return res.data[0] if res.data else None
        except Exception as e:
            print(f"Error creating FAQ: {e}")
            return None

    @staticmethod
    def delete_faq(faq_id: str) -> bool:
        try:
            supabase.table("faq").delete().eq("id", faq_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting FAQ: {e}")
            return False

    # --- ANALYTICS & LOGGING ---
    @staticmethod
    def create_analytics_record(metric_name: str, metric_value: int = 1, details: Optional[Dict[str, Any]] = None) -> bool:
        try:
            data = {
                "metric_name": metric_name,
                "metric_value": metric_value,
                "details": details
            }
            supabase.table("analytics").insert(data).execute()
            return True
        except Exception as e:
            print(f"Error logging analytics record: {e}")
            return False

    @staticmethod
    def get_analytics_summary() -> Dict[str, Any]:
        try:
            # Standard queries for summarizing metrics
            # 1. Total Messages count
            msg_res = supabase.table("messages").select("id", count="exact").execute()
            total_messages = msg_res.count or 0
            
            # 2. Total Sessions / Customers
            cust_res = supabase.table("chat_sessions").select("id", count="exact").execute()
            total_customers = cust_res.count or 0

            # 3. Token usage details
            token_res = supabase.table("analytics").select("metric_value").eq("metric_name", "token_usage").execute()
            total_tokens = sum(item["metric_value"] for item in token_res.data) if token_res.data else 0

            # 4. Today's messages
            today_str = datetime.date.today().isoformat()
            today_res = supabase.table("messages").select("id", count="exact").gte("created_at", today_str).execute()
            today_messages = today_res.count or 0

            # 5. Avg Response Time (if logged)
            time_res = supabase.table("analytics").select("metric_value").eq("metric_name", "response_time_ms").execute()
            avg_response_time = (sum(item["metric_value"] for item in time_res.data) / len(time_res.data)) if time_res.data else 0.0

            return {
                "total_messages": total_messages,
                "today_messages": today_messages,
                "total_customers": total_customers,
                "total_tokens_used": total_tokens,
                "avg_response_time_ms": round(avg_response_time, 2)
            }
        except Exception as e:
            print(f"Error compiling analytics summary: {e}")
            return {}

    @staticmethod
    def create_conversation_log(session_id: str, input_text: str, retrieved_chunks: List[str], output_text: str, tokens_used: int, response_time_ms: int) -> bool:
        try:
            data = {
                "session_id": session_id,
                "input_text": input_text,
                "retrieved_chunks": retrieved_chunks,
                "output_text": output_text,
                "tokens_used": tokens_used,
                "response_time_ms": response_time_ms
            }
            supabase.table("conversation_logs").insert(data).execute()
            # Log separate analytic metrics as well
            DatabaseRepository.create_analytics_record("token_usage", tokens_used, {"session_id": session_id})
            DatabaseRepository.create_analytics_record("response_time_ms", response_time_ms, {"session_id": session_id})
            DatabaseRepository.create_analytics_record("knowledge_search", 1, {"session_id": session_id})
            return True
        except Exception as e:
            print(f"Error creating conversation log: {e}")
            return False

    @staticmethod
    def get_conversation_logs() -> List[Dict[str, Any]]:
        try:
            res = supabase.table("conversation_logs").select("*").order("created_at", desc=True).limit(50).execute()
            return res.data if res.data else []
        except Exception as e:
            print(f"Error fetching conversation logs: {e}")
            return []
    
    @staticmethod
    def get_recent_messages(session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Returns the most recent messages of a chat session.
        Used to provide conversation memory to the AI.
        """
        try:
            res = (
                supabase.table("messages")
                .select("*")
                .eq("session_id", session_id)
                .order("created_at", desc=False)
                .limit(limit)
                .execute()
            )

            return res.data if res.data else []

        except Exception as e:
            print(f"Error fetching recent messages: {e}")
            return []