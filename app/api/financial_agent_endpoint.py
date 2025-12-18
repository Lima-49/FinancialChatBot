from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from app.models.message_models import convert_history
from app.models.research_models import ResearchResponse
from app.services.opena_ai_service import OpenAIService
from app.core.config import log_error_to_file
from app.core.prompts import research_prompt

financial_agent_bp = Blueprint("financialAgent", __name__)

# PROD
research_service = OpenAIService(research_prompt, ResearchResponse)


@financial_agent_bp.route("/bot", methods=["POST"])
def bot():
    """Twilio webhook that routes the message through the financial agent tools."""
    resp = MessagingResponse()
    msg = resp.message()

    try:
        # Twilio sends form-encoded body; fallback to JSON if called directly.
        payload = request.get_json(silent=True) or {}
        incoming_msg = payload.get("query") or request.values.get("Body", "")
        chat_history_raw = payload.get("chat_history")

        if not incoming_msg:
            msg.body("Nenhuma mensagem recebida.")
            return str(resp)

        formatted_history = convert_history(chat_history_raw)
        result = research_service.run(incoming_msg, formatted_history)

        if not result:
            msg.body("Não consegui gerar uma resposta agora. Tente novamente mais tarde.")
            return str(resp)

        response_text = (result.summary)
        msg.body(response_text)
        return str(resp)
    except Exception as e:
        log_error_to_file(e)
        msg.body("Ocorreu um erro no agente financeiro. Tente novamente em instantes.")
        return str(resp)