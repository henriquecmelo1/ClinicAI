from pydantic import BaseModel, Field
from typing import Optional

# --- Modelos Aninhados ---
# É uma boa prática criar classes separadas para objetos JSON internos.

class PatientInfo(BaseModel):
    """Informações demográficas básicas do paciente."""
    nome: Optional[str] = Field(
        default="", 
        description="Nome completo do paciente."
    )
    idade: Optional[int] = Field(
        default="", 
        description="Idade do paciente em anos."
    )

class CollectedData(BaseModel):
    """Estrutura para armazenar todos os dados da triagem coletados durante a conversa."""
    queixa_principal: Optional[str] = Field(default="")
    sintomas_detalhados: Optional[str] = Field(default="")
    duracao_frequencia: Optional[str] = Field(default="")
    intensidade: Optional[str] = Field(default="")
    historico_relevante: Optional[str] = Field(default="")
    historico_familiar: Optional[str] = Field(default="")
    medidas_tomadas: Optional[str] = Field(default="")


# --- Modelo Principal ---
# Este é o modelo que você vinculará ao seu LLM.

class ClinicAIAssistantResponse(BaseModel):
    """
    A resposta estruturada completa do assistente ClinicAI.
    Este formato deve ser usado para cada turno da conversa.
    """
    agent_response: str = Field(
        description="A resposta em texto que deve ser mostrada ao usuário."
    )
    patient_info: PatientInfo = Field(
        default_factory=PatientInfo,
        description="Objeto contendo as informações demográficas do paciente."
    )
    collected_data: CollectedData = Field(
        default_factory=CollectedData,
        description="Objeto contendo todos os dados clínicos coletados na triagem."
    )
    triage_complete: bool = Field(
        default=False,
        description=(
            "Deve ser 'false' durante toda a coleta de dados. "
            "Definir como 'true' APENAS na mensagem final, "
        )
    )