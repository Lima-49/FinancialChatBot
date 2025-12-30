from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from app.models.message_models import convert_history
from app.models.research_models import ResearchResponse
from app.services.opena_ai_service import OpenAIService
from app.services.conversation_history_service import ConversationHistoryService
from app.core.config import log_error_to_file
from app.core.prompts import research_prompt

financial_agent_bp = Blueprint("financialAgent", __name__)

# PROD
research_service = OpenAIService(research_prompt, ResearchResponse)
conversation_service = ConversationHistoryService()


@financial_agent_bp.route("/bot", methods=["POST"])
def bot():
    """Twilio webhook that routes the message through the financial agent tools."""
    resp = MessagingResponse()
    msg = resp.message()

    try:
        payload = request.get_json(silent=True) or {}
        incoming_msg = payload.get("query") or request.values.get("Body", "")
        
        # Obtém o número de telefone do usuário 
        phone_number = payload.get("phone_number") or request.values.get("From", "")

        if not incoming_msg:
            msg.body("Nenhuma mensagem recebida.")
            return str(resp)
        
        if not phone_number:
            msg.body("Não foi possível identificar o número de telefone.")
            return str(resp)

        # Recupera o histórico do banco de dados (últimas 10 mensagens das últimas 24h)
        chat_history = conversation_service.get_history(
            numero_telefone=phone_number,
            limit=10,
            hours_back=24
        )
        
        # Converte para o formato esperado pelo LangChain
        formatted_history = convert_history(chat_history)
        
        # Salva a mensagem do usuário no banco
        conversation_service.save_message(
            numero_telefone=phone_number,
            tipo_mensageiro="user",
            conteudo_mensagem=incoming_msg
        )
        
        # Processa a mensagem com o agente
        result = research_service.run(incoming_msg, formatted_history)

        if not result:
            msg.body("Não consegui gerar uma resposta agora. Tente novamente mais tarde.")
            return str(resp)

        response_text = result.summary
        
        # Salva a resposta do assistente no banco
        conversation_service.save_message(
            numero_telefone=phone_number,
            tipo_mensageiro="assistant",
            conteudo_mensagem=response_text
        )
        
        msg.body(response_text)
        return str(resp)
    except Exception as e:
        log_error_to_file(e)
        msg.body("Ocorreu um erro no agente financeiro. Tente novamente em instantes.")
        return str(resp)