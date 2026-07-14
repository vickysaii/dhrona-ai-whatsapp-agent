import redis
import json
from typing import List, Dict, Any
from app.config import settings

class RedisMemoryService:
    def __init__(self):
        try:
            self.client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
                db=settings.REDIS_DB,
                decode_responses=True,
                socket_timeout=2
            )
            # Ping to verify connection
            self.client.ping()
            self.enabled = True
            print("Connected to Redis successfully for conversation memory.")
        except Exception as e:
            print(f"Warning: Redis is unavailable ({e}). Falling back to simple in-memory session backup.")
            self.client = None
            self.enabled = False
            self.fallback_db: Dict[str, List[Dict[str, str]]] = {}

    def get_history(self, customer_phone: str, limit: int = 10) -> List[Dict[str, str]]:
        """
        Retrieves the rolling conversation history as a list of roles and content.
        Example output: [{"role": "user", "content": "hello"}, {"role": "model", "content": "hi"}]
        """
        key = f"wa_chat_history:{customer_phone}"
        if self.enabled and self.client:
            try:
                history_data = self.client.lrange(key, 0, limit - 1)
                # Redis returns them in order; parse JSON
                return [json.loads(msg) for msg in reversed(history_data)]
            except Exception as e:
                print(f"Error fetching history from Redis: {e}")
        
        # Fallback to local memory
        return self.fallback_db.get(customer_phone, [])[-limit:]

    def add_message(self, customer_phone: str, role: str, content: str, limit: int = 10) -> None:
        """
        Pushes a new message onto the conversation list and prunes it to the limit.
        role: 'user' or 'model' (matching Gemini roles)
        """
        key = f"wa_chat_history:{customer_phone}"
        message_obj = {"role": role, "content": content}
        message_str = json.dumps(message_obj)
        
        if self.enabled and self.client:
            try:
                # Push message to head of list
                self.client.lpush(key, message_str)
                # Trim list to keep only latest limit items
                self.client.ltrim(key, 0, limit - 1)
                # Set TTL of 24 hours on conversation history
                self.client.expire(key, 86400)
                return
            except Exception as e:
                print(f"Error writing message to Redis: {e}")

        # Fallback to local memory
        if customer_phone not in self.fallback_db:
            self.fallback_db[customer_phone] = []
        self.fallback_db[customer_phone].append(message_obj)
        if len(self.fallback_db[customer_phone]) > limit:
            self.fallback_db[customer_phone] = self.fallback_db[customer_phone][-limit:]

    def clear_memory(self, customer_phone: str) -> None:
        """
        Clears memory for a specific phone number.
        """
        key = f"wa_chat_history:{customer_phone}"
        if self.enabled and self.client:
            try:
                self.client.delete(key)
            except Exception as e:
                print(f"Error deleting Redis key: {e}")
        
        if customer_phone in self.fallback_db:
            del self.fallback_db[customer_phone]

redis_memory = RedisMemoryService()
