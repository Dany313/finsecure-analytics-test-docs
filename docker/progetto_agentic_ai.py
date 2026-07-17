import os
import json
import html
import re
from typing import List, Dict, Optional
import requests

from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools.retriever import create_retriever_tool
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_classic.memory import ConversationSummaryMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator


def get_secret(key_name):
    return os.environ.get(key_name)


providers = [
    {"name": "gemini", "env_var": "GEMINI_API_KEY", "lib": "langchain-google-genai"},
    {"name": "openai", "env_var": "OPENAI_API_KEY", "lib": "langchain-openai"},
    {"name": "groq",   "env_var": "GROQ_API_KEY", "lib": "langchain-groq"}
]

os.environ["ACTIVE_LLM"] = ""

for provider in providers:
    api_key = get_secret(provider["env_var"])
    if api_key:
        os.environ[provider["env_var"]] = api_key
        os.environ["ACTIVE_LLM"] = provider["name"]
        print(f"API Key di {provider['name'].capitalize()} configurata")
        break

if not os.environ["ACTIVE_LLM"]:
    raise ValueError("ERRORE CRITICO: Nessuna API key trovata per Gemini, OpenAI o Groq tra le variabili d'ambiente. L'esecuzione non può proseguire.")


COMPANY_DOCS_FOLDER = "RAG_database/company_docs"
EMBED_MODEL = "all-MiniLM-L6-v2"

GEMINI_MODEL = "gemini-3.1-flash-lite"
OPENAI_MODEL = "gpt-5.4-mini"
GROQ_MODEL = "llama-3.1-8b-instant"

llm = None

match os.environ.get("ACTIVE_LLM"):
    case "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL, temperature=0.1)
        print(f"LLM impostato su Google Gemini ({GEMINI_MODEL})")
    case "openai":
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0.1)
        print(f"LLM impostato su OpenAI ({OPENAI_MODEL})")
    case "groq":
        from langchain_groq import ChatGroq
        llm = ChatGroq(model=GROQ_MODEL, temperature=0.1)
        print(f"LLM impostato su Groq ({GROQ_MODEL})")

if not llm:
    raise ValueError("Nessun LLM attivo configurato. Verifica le variabili d'ambiente.")

repo_test_docs_url = 'https://github.com/Dany313/finsecure-analytics-test-docs.git'
docs_folder = 'RAG_database'

if not os.path.exists(docs_folder):
    os.system(f"git clone {repo_test_docs_url} {docs_folder}")
    print("Dataset clonato con successo")
else:
    print("Dataset già presente")

lc_embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
lc_vector_store = Chroma(
    persist_directory= docs_folder + "/chroma_db_langchain",
    embedding_function=lc_embeddings
)
lc_retriever = lc_vector_store.as_retriever(search_kwargs={"k": 3})


class FinancialAnalysisInput(BaseModel):
    content: str = Field(..., description="Il testo o il contenuto del/i report finanziario/i da analizzare.")


class FinancialAnalysisOutput(BaseModel):
    kpis: Dict[str, float] = Field(..., description="Dizionario dei Key Performance Indicators (es. 'tasso_interesse': 4.25).")
    anomalies: List[str] = Field(..., description="Eventuali anomalie, debolezze o rischi identificati nel testo.")
    summary: str = Field(..., description="Sintesi esecutiva dell'analisi.")


class RiskSimulationInput(BaseModel):
    content: str = Field(..., description="Descrizione del portafoglio azionario o degli asset su cui effettuare la simulazione.")
    portfolio_value: float = Field(..., description="Valore totale in dollari/euro del portafoglio (deve essere > 0).", gt=0)
    scenario: str = Field(..., description="Scenario di stress da applicare, es. 'tech_crash', 'recession', 'rate_hike'.")


class RiskSimulationOutput(BaseModel):
    estimated_impact: float = Field(..., description="La perdita (o guadagno) stimata in valore assoluto.")
    post_shock_value: float = Field(..., description="Il valore del portafoglio stimato dopo lo shock.")
    reasoning: str = Field(..., description="Spiegazione logica di come il portafoglio ha reagito allo shock in base alla sua composizione.")


class WebSearchInput(BaseModel):
    query: str = Field(..., description="La query di ricerca da effettuare sul web.")


class DocumentRetrievalInput(BaseModel):
    query: str = Field(..., description="Parola chiave per cercare i documenti aziendali (es. 'portfolio', 'market'). Il tool recupererà in automatico tutti i file il cui nome contiene questa parola.")


class DocumentRetrievalOutput(BaseModel):
    documents_content: Dict[str, str] = Field(..., description="Dizionario con chiave il nome del file e valore il suo contenuto testuale completo.")


@tool("analyze_financial_reports", args_schema=FinancialAnalysisInput)
def analyze_financial_reports(content: str) -> str:
    """
    Analisi automatizzata dei report finanziari: estrazione di KPI e identificazione di anomalie.
    Prende in input una stringa contenente uno o più documenti.
    Ritorna un JSON validato coerente con lo schema FinancialAnalysisOutput.
    """
    kpis = {}
    anomalies = []

    content_upper = content.upper()
    if "USA" in content_upper or "STATI UNITI" in content_upper:
        kpis = {"interest_rate_fed": 4.25, "inflation": 2.1, "sp500_growth": 8.0}
        anomalies = ["Forte concentrazione del rischio sui titoli tech (Magnifici 7).", "Tensioni geopolitiche e dazi sui semiconduttori."]
        summary = "Il mercato USA mostra un soft landing, ma la dipendenza dal settore tech è un fattore di rischio critico."

    elif "CINA" in content_upper or "PBOC" in content_upper:
        kpis = {"gdp_growth": 4.2, "real_estate_drop": -4.0, "ev_export_growth": 15.0}
        anomalies = ["Disoccupazione giovanile oltre l'11%.", "Crisi strutturale del mercato immobiliare non risolta dagli stimoli."]
        summary = "Nonostante i massicci stimoli della PBOC, il mercato cinese sconta pesanti freni normativi e immobiliari, salvato solo dall'export di EV."

    else:
        kpis = {"words_count": float(len(content.split()))}
        anomalies = ["Dati insufficienti o contesto non riconosciuto per un'estrazione mirata."]
        summary = "Analisi generica completata. Non sono stati individuati pattern macroeconomici noti."

    output_model = FinancialAnalysisOutput(kpis=kpis, anomalies=anomalies, summary=summary)

    return output_model.model_dump_json(indent=2)


@tool("simulate_risk_scenario", args_schema=RiskSimulationInput)
def simulate_risk_scenario(content: str, portfolio_value: float, scenario: str) -> str:
    """
    Simulazione scenari di rischio: modellazione di possibili impatti finanziari in base ai dati storici e a variabili economiche.
    Prende in input la composizione del portafoglio (testo), il valore nominale e lo scenario.
    Ritorna un JSON validato coerente con lo schema RiskSimulationOutput.
    """
    scenario_lower = scenario.lower()
    content_lower = content.lower()

    impact_factor = 0.0
    reasoning = ""

    is_tech_heavy = "tech" in content_lower or "nvidia" in content_lower or "cloud" in content_lower
    is_defensive = "dividend" in content_lower or "healthcare" in content_lower or "consumer staples" in content_lower

    if "crash" in scenario_lower or "crollo" in scenario_lower or "bubble" in scenario_lower:
        if is_tech_heavy:
            impact_factor = -0.25
            reasoning = "Il portafoglio ha un'altissima esposizione al settore tecnologico e Growth, subendo pesantemente il crollo dei multipli."
        elif is_defensive:
            impact_factor = -0.05
            reasoning = "La natura difensiva del portafoglio (Value/Dividendi) attutisce fortemente l'impatto del crollo di mercato."
        else:
            impact_factor = -0.15
            reasoning = "Impatto di mercato medio per un portafoglio bilanciato."

    elif "recession" in scenario_lower or "recessione" in scenario_lower:
        if is_defensive:
            impact_factor = -0.03
            reasoning = "Asset anelastici (Healthcare, Utilities) reggono bene la flessione dei consumi."
        else:
            impact_factor = -0.12
            reasoning = "Le aziende cicliche e growth subiscono il calo della domanda aggregata."
    else:
        impact_factor = -0.02
        reasoning = f"Impatto lieve stimato per lo scenario non standardizzato '{scenario}'."

    estimated_impact = portfolio_value * impact_factor
    post_shock_value = portfolio_value + estimated_impact

    output_model = RiskSimulationOutput(
        estimated_impact=estimated_impact,
        post_shock_value=post_shock_value,
        reasoning=reasoning
    )
    return output_model.model_dump_json(indent=2)


@tool("search_web", args_schema=WebSearchInput)
def search_web(query: str) -> str:
    """
    Cerca su internet informazioni aggiornate, dati macroeconomici, o definizioni finanziarie tramite DuckDuckGo.
    """
    try:
        search = DuckDuckGoSearchRun()
        result = search.invoke(query)
        if not result:
            return "Nessun risultato trovato sul web."
        return result
    except Exception as e:
        return f"Errore durante la ricerca web: {str(e)}"


@tool("retrieve_company_documents", args_schema=DocumentRetrievalInput)
def retrieve_company_documents(query: str) -> str:
    """
    Recupera i documenti aziendali archiviati nella directory 'company_docs'
    cercando la 'query' fornita all'interno dei nomi dei file disponibili.
    """
    base_dir = COMPANY_DOCS_FOLDER
    docs_content = {}

    if not os.path.exists(base_dir):
        return json.dumps({"error": f"La directory '{base_dir}' non esiste."})

    all_files = os.listdir(base_dir)
    matched_files = [f for f in all_files if query.lower() in f.lower() and f.endswith(".txt")]

    if not matched_files:
        return json.dumps({"error": f"Nessun documento trovato con la chiave '{query}'. File disponibili: {', '.join(all_files)}"})

    for doc_name in matched_files:
        filepath = os.path.join(base_dir, doc_name)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                docs_content[doc_name] = f.read()
        except Exception as e:
            docs_content[doc_name] = f"Errore nella lettura del file: {str(e)}"

    output_model = DocumentRetrievalOutput(documents_content=docs_content)
    return output_model.model_dump_json(indent=2)


rag_financial_audit_tool = create_retriever_tool(
    lc_retriever,
    "rag_financial_audit",
    "Usa questo tool per cercare informazioni sui documenti finanziari, normative (Basilea III, ecc), report aziendali, crisi storiche, e policy interne dell'azienda."
)

tools = [
    rag_financial_audit_tool,
    analyze_financial_reports,
    simulate_risk_scenario,
    search_web,
    retrieve_company_documents
]
print(f"Definiti {len(tools)} tools")

system_prompt = """
Sei l'Assistente AI di FinSecure Analytics, specializzato in gestione del rischio finanziario e audit interattivi.
Hai accesso a dei tool specifici:
- `analyze_financial_reports`: usalo SEMPRE quando l'utente chiede informazioni su normative, policy aziendali o analisi storiche.
- `simulate_risk_scenario`: usalo SEMPRE quando ti viene chiesta una simulazione di impatto sul portafoglio, un calo o una crescita percentuale.
- `search_web`: usalo SE NECESSARIO se necessario per rispondere alla domanda o per aggiungere informazioni se non disponi della conoscenza necessaria.
- `retrieve_company_documents`: usalo SE NECESSARIO per ricercare tra i documenti aziendali uno o piu documenti specifici.

Sii sempre preciso, professionale e analitico.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

memory = ConversationSummaryMemory(
    llm=llm,
    memory_key="chat_history",
    return_messages=True
)

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)

print("Agente inizializzato...")

app = FastAPI(title="FinSecure AI Chat API")


class ChatRequest(BaseModel):
    message: str = Field(..., max_length=1000, description="Il messaggio testuale dell'analista")

    @field_validator('message')
    @classmethod
    def sanitize_message(cls, v: str) -> str:
        sanitized = v.strip()
        if not sanitized:
            raise ValueError('Il messaggio non può essere vuoto o composto solo da spazi.')
        sanitized = re.sub(r'<[^>]*>', '', sanitized)
        sanitized = html.escape(sanitized)
        return sanitized


class ChatResponse(BaseModel):
    response: str


class MemoryResetResponse(BaseModel):
    status: str


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        res = agent_executor.invoke({"input": request.message})

        output_data = res.get("output", "")
        if isinstance(output_data, list):
            parts = []
            for item in output_data:
                if isinstance(item, dict) and "text" in item:
                    parts.append(str(item["text"]))
                elif isinstance(item, str):
                    parts.append(item)
                else:
                    parts.append(str(item))
            text_output = "".join(parts)
        else:
            text_output = str(output_data)

        return ChatResponse(response=text_output)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/chat/memory", response_model=MemoryResetResponse)
async def reset_memory_endpoint():
    memory.clear()
    return MemoryResetResponse(status="Memoria dell'agente svuotata con successo.")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)