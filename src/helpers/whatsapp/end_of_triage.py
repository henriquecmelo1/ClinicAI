from ...services.database_service import add_conversation_summary
from ...routers.whatsapp_router import send_whatsapp_message
from ...models.response_model import PatientInfo, CollectedData
import dotenv
import os

dotenv.load_dotenv()

RECIPIENT_WAID = os.getenv("RECIPIENT_WAID") # número que recebe a mensagem (médico)

async def end_of_triage(conversation_id, sender_id: str, collected_data: CollectedData, patient_info: PatientInfo):
    try:

        formatted_data = {
            "Nome": patient_info.nome,
            "Idade": patient_info.idade,
            "Queixa Principal": collected_data.queixa_principal,
            "Sintomas Detalhados": collected_data.sintomas_detalhados,
            "Duração e Frequência": collected_data.duracao_frequencia,
            "Intensidade": collected_data.intensidade,
            "Histórico Relevante": collected_data.historico_relevante,
            "Histórico Familiar": collected_data.historico_familiar,
            "Medidas Tomadas": collected_data.medidas_tomadas
        }


        formatted_response = (
            f"Triagem do paciente *{formatted_data['Nome']}*.\n\n"
            f"Idade: {formatted_data['Idade']}\n"
            f"Dados Coletados:\n"
            f"- Queixa Principal: {formatted_data['Queixa Principal']}\n"
            f"- Sintomas Detalhados: {formatted_data['Sintomas Detalhados']}\n"
            f"- Duração e Frequência: {formatted_data['Duração e Frequência']}\n"
            f"- Intensidade: {formatted_data['Intensidade']}\n"
            f"- Histórico Relevante: {formatted_data['Histórico Relevante']}\n"
            f"- Histórico Familiar: {formatted_data['Histórico Familiar']}\n"
            f"- Medidas Tomadas: {formatted_data['Medidas Tomadas']}\n"
            "\nPor favor, revise as informações coletadas e prossiga com os próximos passos."
        )

        

        await add_conversation_summary(conversation_id, sender_id, formatted_data)
        await send_whatsapp_message(formatted_response, RECIPIENT_WAID)
    except Exception as e:
        print(f"Error adding conversation summary: {e}")