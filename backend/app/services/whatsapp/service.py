import httpx

from app.config import settings


class WhatsAppService:

    BASE_URL = "https://graph.facebook.com/v23.0"

    @staticmethod
    async def send_text_message(
        phone_number: str,
        message: str,
    ):

        url = (
            f"{WhatsAppService.BASE_URL}/"
            f"{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
        )

        headers = {
            "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }

        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message,
            },
        }

        print("\n========== Sending WhatsApp Message ==========")
        print(f"To      : {phone_number}")
        print(f"Message : {message}")
        print("==============================================")

        async with httpx.AsyncClient(timeout=30) as client:

            response = await client.post(
                url=url,
                headers=headers,
                json=payload,
            )

        print("\n========== WhatsApp API Response ==========")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        print("===========================================\n")

        response.raise_for_status()

        return response.json()