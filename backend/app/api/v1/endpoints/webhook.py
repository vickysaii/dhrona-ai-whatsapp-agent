from fastapi import APIRouter, Request, Response, BackgroundTasks, status
from fastapi.responses import PlainTextResponse
from app.config import settings
from app.agents.business_agent import BusinessAgent
from typing import Dict, Any

router = APIRouter()


@router.get("/webhook", response_class=PlainTextResponse)
def verify_webhook(request: Request):
    """
    Handles WhatsApp Webhook verification GET challenge.
    """

    params = request.query_params

    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    # -----------------------------
    # DEBUG
    # -----------------------------
    print("\n========== WEBHOOK VERIFICATION ==========")
    print("Meta Mode :", mode)
    print("Meta Token:", token)
    print("ENV Token :", settings.WHATSAPP_VERIFY_TOKEN)
    print("==========================================\n")

    if mode and token:

        if mode == "subscribe" and token == settings.WHATSAPP_VERIFY_TOKEN:
            print("✅ Webhook verified successfully!")
            return challenge

        else:
            print("❌ Webhook verification failed: token mismatch.")
            return Response(
                content="Verification token mismatch",
                status_code=status.HTTP_403_FORBIDDEN
            )

    return Response(
        content="Invalid parameters",
        status_code=status.HTTP_400_BAD_REQUEST
    )


@router.post("/webhook")
async def receive_webhook(
    request: Request,
    background_tasks: BackgroundTasks
):
    """
    Receives incoming WhatsApp events.
    """

    try:

        payload = await request.json()

        print("\n========== INCOMING WEBHOOK ==========")
        print(payload)
        print("======================================\n")

        if payload.get("object") != "whatsapp_business_account":
            return {"status": "ignored"}

        entry_list = payload.get("entry", [])

        for entry in entry_list:

            changes = entry.get("changes", [])

            for change in changes:

                value = change.get("value", {})

                # -----------------------------
                # Status Updates
                # -----------------------------
                if "statuses" in value:

                    for status_item in value["statuses"]:

                        print(
                            f"Status Update: {status_item.get('status')} "
                            f"for {status_item.get('recipient_id')}"
                        )

                    continue

                # -----------------------------
                # Incoming Messages
                # -----------------------------
                if "messages" not in value:
                    continue

                contacts = value.get("contacts", [])

                contact_name = "WhatsApp User"

                if contacts:
                    contact_name = contacts[0].get(
                        "profile",
                        {}
                    ).get(
                        "name",
                        "WhatsApp User"
                    )

                for msg in value["messages"]:

                    from_phone = msg.get("from")
                    msg_id = msg.get("id")
                    msg_type = msg.get("type")

                    # -----------------------------
                    # Text Message
                    # -----------------------------
                    if msg_type == "text":

                        body = msg["text"].get("body", "")

                        print(f"\nMessage From : {from_phone}")
                        print(f"Customer     : {contact_name}")
                        print(f"Text         : {body}\n")

                        # We will implement this in the next step
                        background_tasks.add_task(
                            BusinessAgent.process_incoming_message,
                            from_phone,
                            contact_name,
                            body,
                            msg_id,
                        )

        return {"status": "received"}

    except Exception as e:

        print(f"Webhook Error: {e}")

        return {
            "status": "error",
            "detail": str(e)
        }