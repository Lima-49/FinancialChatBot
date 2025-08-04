from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import Tool
from datetime import datetime

def save_to_txt(data:str, filename:str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    formated_text = f" --- Research Output - {timestamp} --- \n\n{data}\n"

    with open(filename, "a", encoding="utf-8") as file:
        file.write(formated_text)

    return f"Data saved to {filename}"

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="SearchDuckDuckGo",
    func=search.run,
    description="Search the web using DuckDuckGo. Provide a query to get search results."
)

save_tool = Tool(
    name="SaveToTxt",
    func=save_to_txt,
    description="Saves the research output to a text file. Provide the data to save."
)

api_wrapper = WikipediaAPIWrapper(top_k_results=5, doc_content_chars_max=1000)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

