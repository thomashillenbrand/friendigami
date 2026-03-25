"""Twilio SMS webhook routes."""
from fastapi import APIRouter, Depends, Form, Response
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.combination_service import CombinationService

router = APIRouter(prefix="/sms", tags=["sms"])


def twiml_response(message: str) -> Response:
    """Wrap a message in TwiML XML response."""
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        "<Response>"
        f"<Message>{message}</Message>"
        "</Response>"
    )
    return Response(content=xml, media_type="application/xml")


@router.post("/webhook")
def sms_webhook(Body: str = Form(""), db: Session = Depends(get_db)) -> Response:
    """Handle incoming Twilio SMS.

    Expected format: comma-separated friend symbols, e.g. "TH, MW, RZ"
    """
    raw = Body.strip()
    if not raw:
        return twiml_response("Please send friend symbols separated by commas (e.g. TH, MW, RZ)")

    symbols = [s.strip().upper() for s in raw.split(",") if s.strip()]

    if len(symbols) < 2:
        return twiml_response("Need at least 2 friend symbols separated by commas.")

    service = CombinationService(db)
    combo, was_already = service.mark_occurred_by_symbols(symbols)

    if combo is None:
        return twiml_response(
            f"Combination not found for: {', '.join(symbols)}. "
            "Check that all symbols are valid."
        )

    if was_already:
        return twiml_response(f"Already happened! ({combo.id})")

    return twiml_response(f"New combination logged! ({combo.id})")
