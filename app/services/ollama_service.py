from langchain_ollama.llms import OllamaLLM

llm = OllamaLLM(model="llama2")

def run_ollama_research(query: str):
    response = llm.invoke(query)
    return {"response": response}