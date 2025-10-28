# ClinicAI - WhatsApp Medical Assistant Chatbot

ClinicAI é um chatbot inteligente desenvolvido para triagem de consultas médicas através do WhatsApp. O sistema utiliza tecnologias avançadas de IA para processar mensagens de texto, fornecendo respostas contextualizadas e auxiliando em triagens de consultas. Como funcionalidade adicional, também suporta transcrição e processamento de mensagens de áudio.

## 🚀 Tecnologias Utilizadas

- **FastAPI**: Framework web para criação da API REST
- **LangGraph**: Orquestração de fluxos de conversação e análise de mensagens
- **Google Gemini**: LLM para geração de respostas inteligentes
- **WhatsApp Business API**: Integração com a plataforma de mensagens da Meta
- **MongoDB**: Banco de dados para armazenamento de conversas e dados
- **OpenAI Whisper**: Transcrição de mensagens de áudio (feature adicional)
- **Python**: Linguagem de programação principal

## 📋 Funcionalidades

- 💬 **Recebimento e envio de mensagens de texto** via WhatsApp Business API
- 🧠 **Análise inteligente de mensagens** com LangGraph
- 🤖 **Respostas contextualizadas** geradas pelo Google Gemini
- 📊 **Armazenamento de conversas** em MongoDB
- 🔄 **Fluxo de triagem médica** automatizado
- 🎤 **Transcrição de mensagens de áudio** usando OpenAI Whisper

## 🎥 Demonstração

Veja abaixo uma demonstração em vídeo do funcionamento do ClinicAI:

[![Demonstração do ClinicAI](https://img.youtube.com/vi/placeholder/0.jpg)](public/demo.mp4)

---

## 🛠️ Instalação e Configuração

### Pré-requisitos

- Python 3.8+
- ngrok (para tunelamento local)
- Conta no Meta for Developers
- API Key do Google Gemini
- MongoDB (local ou na nuvem)
- FFMPEG (para manipulação de arquivos de áudio)
  - Baixe em: https://ffmpeg.org/download.html
  - **⚠️ Importante**: Adicione o FFMPEG às variáveis de ambiente do sistema (PATH)
  - Para verificar se está instalado: `ffmpeg -version` no terminal

### 1. Clone o repositório

```bash
git clone https://github.com/henriquecmelo1/ClinicAI.git
cd ClinicAI
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configuração do Meta for Developers

1. Acesse [Meta for Developers](https://developers.facebook.com/)
2. Crie um novo aplicativo para WhatsApp Business
3. Configure o webhook URL (será fornecida pelo ngrok)
4. Obtenha as credenciais necessárias (APP_ID, APP_SECRET, ACCESS_TOKEN, etc.)

#### 3.1 Configuração de Números de Telefone

Para enviar mensagens via API, é necessário cadastrar os números de telefone:

1. No painel do aplicativo, acesse **WhatsApp → Configuração da API**
2. Na seção "Números de telefone", adicione o número que receberá as mensagens
3. **Ativação do número**: 
   - Envie uma mensagem template pelo painel do Meta for Developers
   - Responda a mensagem template em seu telefone
   - Após esta interação, o número estará ativo e pronto para receber mensagens da aplicação

> **⚠️ Importante**: Sem este processo de ativação, a API não conseguirá enviar mensagens para o número cadastrado.

### 4. Configuração das variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto baseado no arquivo `.env.example`:

```bash
cp .env.example .env
```

Preencha as seguintes variáveis no arquivo `.env`:

#### Meta API Credentials (WhatsApp Business API)
- `ACCESS_TOKEN`: Token de acesso temporário do Meta for Developers
- `RECIPIENT_WAID`: Número de telefone do médico (ex: 5581912341234)
- `APP_ID`: ID do aplicativo Meta
- `APP_SECRET`: Secret do aplicativo Meta
- `API_VERSION`: Versão da API (ex: v22.0)
- `PHONE_NUMBER_ID`: ID do número de teste da Meta
- `VERIFY_TOKEN`: Token de verificação para webhook

#### Google Gemini
- `GOOGLE_API_KEY`: Chave da API do Google Gemini

#### MongoDB
- `MONGO_URI`: String de conexão do MongoDB (ex: mongodb://localhost:27017/ClinicAI)

### 5. Configuração do ngrok

O ngrok é necessário para criar um túnel entre a API do WhatsApp e seu localhost:

1. Instale o ngrok: https://ngrok.com/download
2. Execute o ngrok para expor sua aplicação:

```bash
ngrok http 8000
```

3. Use a URL fornecida pelo ngrok para configurar o webhook no Meta for Developers

## 🚀 Executando a aplicação

### 1. Inicie a aplicação

```bash
uvicorn src.main:app --reload --port 8000
```

### 2. Em outro terminal, inicie o ngrok

```bash
ngrok http 8000
```

### 3. Configure o webhook

Configure a URL do webhook no Meta for Developers usando a URL fornecida pelo ngrok:
```
https://your-ngrok-url.ngrok.io/webhook
```

## 📁 Estrutura do Projeto

```
ClinicAI/
├── src/
│   ├── main.py                 # Ponto de entrada da aplicação
│   ├── config/                 # Configurações do sistema
│   │   ├── database.py         # Configuração do MongoDB
│   │   ├── langgraph_config.py # Configuração do LangGraph
│   │   └── prompt.py           # Prompt de configuração do agente
│   ├── helpers/                # Funções auxiliares
│   │   ├── ai/                 # Helpers de IA
│   │   └── whatsapp/           # Handlers do WhatsApp
│   ├── models/                 # Modelos de dados
│   ├── routers/                # Endpoints da API
│   │   ├── webhook_router.py   # Rotas do webhook
│   │   └── whatsapp_router.py  # Rotas do WhatsApp
│   └── services/               # Serviços de negócio
├── whatsapp_audio_files/       # Arquivos de áudio temporários
├── requirements.txt            # Dependências do projeto
└── .env.example               # Exemplo de variáveis de ambiente
```

## 🔧 Como funciona

1. **Recebimento de mensagens**: O WhatsApp envia mensagens  via webhook para a aplicação
2. **Processamento de áudio**: Mensagens de áudio são transcritas usando OpenAI Whisper e a transcrição é processada como uma mensagem de texto
3. **Análise com LangGraph**: As mensagens de texto são processadas pelo fluxo do LangGraph
4. **Geração de resposta**: O Google Gemini gera respostas contextualizadas baseadas no contexto de triagem médica
5. **Envio de resposta**: A resposta é enviada de volta via WhatsApp Business API
6. **Armazenamento**: As conversas são salvas no MongoDB para histórico
7. **Fim da Triagem**: O agente informa quando a triagem médica é concluída e envia as informações necessárias ao médico

## 📝 Endpoints da API

- `GET /`: Health check da aplicação
- `POST /webhook`: Recebe mensagens do WhatsApp (webhook do Meta)
- `GET /webhook`: Verificação do webhook para configuração inicial
- `POST /whatsapp/send-message`: Envia mensagem de texto para um usuário específico


> `POST /whatsapp/send-first-message`: Envia mensagem template inicial (Não está sendo utilizado no fluxo atual)

### Funcionalidades dos Endpoints

**Webhook (`/webhook`)**
- Recebe e processa mensagens de texto e áudio
- Gerencia verificação de tokens para segurança
- Processa mensagens em background para melhor performance

**WhatsApp API (`/whatsapp/`)**
- Integração direta com a API do WhatsApp Business
- Envio de mensagens template e personalizadas
- Gerenciamento de sessões e histórico de conversas

