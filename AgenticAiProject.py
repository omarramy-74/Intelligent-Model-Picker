
from langchain_community.chat_models import ChatOpenAI
from langchain_classic.prompts import ChatPromptTemplate,PromptTemplate
import os
from typing import TypedDict,Dict,List,Any,Optional
from langgraph.graph import StateGraph
import pandas as pd
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import find_dotenv,load_dotenv
path = find_dotenv(filename="secret.env")
load_dotenv(path)
tavily_key = os.getenv("web_search_key")
colab_api_key = os.getenv("Open_Ai_Key")
search_tool = TavilySearchResults(max_results=3,tavily_api_key=tavily_key)

SCORES = [
    
    ("nvidia/nemotron-3-nano-30b-a3b:free",            [7,  8,   7,  7,  8,  7]),
    ("nvidia/nemotron-nano-12b-v2-vl:free",            [6,  6,   6,  5,  6,  7]),
    ("nvidia/nemotron-nano-9b-v2:free",                [6,  6,   6,  5,  7,  6]),
    ("mistralai/mistral-small-3.1-24b-instruct:free",  [7,  7,   8,  7,  7,  7]),
    ("arcee-ai/trinity-mini:free",                     [6,  6,   7,  7,  6,  6]),
    ("z-ai/glm-4.5-air:free",                          [7,  7,   7,  6,  7,  7]),
    ("liquid/lfm-2.5-1.2b-thinking:free",              [5,  7,   4,  4,  6,  5]),
    ("liquid/lfm-2.5-1.2b-instruct:free",              [4,  4,   4,  3,  4,  4]),
    ("stepfun/step-3.5-flash:free",                    [4,  6,   7,  3,  4,  5]),

]


CATEGORIES = ["Global", "Reasoning", "Coding", "Agentic Coding", "Mathematics", "Data Analysis"]

df = pd.DataFrame(
    [{"Model": m, **{f"{cat} Average": s[i] for i, cat in enumerate(CATEGORIES)}}
     for m, s in SCORES]
)

df.head(15)

df.shape


model = ChatOpenAI(
    model_name="arcee-ai/trinity-large-preview:free",
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=colab_api_key,
)

class State(TypedDict):
  message:       str
  classify:      str
  needs_search:  str
  search_result: Optional[str]
  column:        str
  model:         str
  response:      str

graph = StateGraph(State)

def Classify_Input(state:State)->State:
  template = PromptTemplate(
      input_variables=["query"],
      template=(
          """Classify the following query into one of those 6 types
          1-Global(if you cant certainly classify what is the type of the query)
          2-Reasoning
          3-Coding
          4-Agentic Coding
          5-Mathematics
          6-Data Analysis
          """
          "Do not answer the Query.\n"
          "return only the query classified type.\n\n"
          "Original query: {query}"
      )
  )
  chain = template | model
  ans = chain.invoke({"query":state["message"]})
  state['classify'] = ans.content
  state['column'] = state['classify']+" Average"
  return state

def decide_search(state:State)->State:
  template = PromptTemplate(
      input_variables=["query"],
      template=(
         "Does the following Query Require Web Search "
         "from the internet (Live data, current events,up to date information)?\n\n"
         "Answer only using Yes or No.\n\n Query:{query}"
      )
  )
  result = (template | model).invoke({"query": state["message"]}).content.strip().lower()
  state['needs_search'] = 'yes' if 'yes' in result else 'no'
  return state

def run_search(state: State) -> State:
    results = search_tool.invoke(state["message"])
    context = "\n".join(
        f"[{i+1}] {r['url']}\n{r['content']}" for i, r in enumerate(results)
    )
    state["search_result"] = context
    state["message"] = (
        f"{state['message']}\n\n"
        f"--- Web search results (use as context) ---\n{context}"
    )
    return state

def choose_model(state: State) -> State:
    col = state["column"]
    if col not in df.columns:
        col = "Global Average"
    idx = df[col].idxmax()
    state["model"] = df.loc[idx, "Model"]
    return state

def run_model(state: State) -> State:
    model = ChatOpenAI(
        model_name=state["model"],
        openai_api_base="https://openrouter.ai/api/v1",
        openai_api_key=colab_api_key,
    )
    state["response"] = model.invoke(state["message"]).content
    return state

def route(state: State) -> str:
    return "run_search" if state["needs_search"] == "yes" else "choose_model"

"""#**Create Graph**"""

graph = StateGraph(State)

graph.add_node("classify",Classify_Input)
graph.add_node("decide_search",decide_search)
graph.add_node("run_search",run_search)
graph.add_node("choose_model",choose_model)
graph.add_node("run_model",run_model)

graph.set_entry_point("classify")
graph.set_finish_point("run_model")
graph.add_edge("classify","decide_search")
graph.add_conditional_edges(
    "decide_search",
    route,
    {"run_search": "run_search", "choose_model": "choose_model"},
)
graph.add_edge("run_search",   "choose_model")
graph.add_edge("choose_model", "run_model")

app = graph.compile()

app

def ask(query: str) -> dict:
    result = app.invoke({
        "message":       query,
        "classify":      "",
        "needs_search":  "",
        "search_result": None,
        "column":        "",
        "model":         "",
        "response":      "",
    })
    print(f"Type      : {result['classify']}")
    print(f"Search?   : {result['needs_search']}")
    print(f"Model used: {result['model']}")
    print(f"\nResponse:\n{result['response']}")
    return result

if __name__ == "__main__":
    query = input("Enter your query: ")
    ask(query)