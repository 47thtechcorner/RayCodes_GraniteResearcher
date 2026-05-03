import ollama
import sys
from duckduckgo_search import DDGS
import json

# --- CONFIGURATION ---
PLANNER_MODEL = "gemma4:e2b"
SYNTHESIZER_MODEL = "granite-direct"
OUTPUT_FILE = "research_report.md"

def check_models():
    """Check if required models are available in Ollama."""
    try:
        response = ollama.list()
        # The library returns a ListResponse object with a 'models' attribute
        # Each model in the list has a 'model' attribute (which is the name)
        available_models = [m.model for m in response.models]
        
        for required in [PLANNER_MODEL, SYNTHESIZER_MODEL]:
            # Check for exact match or with :latest suffix
            if required not in available_models and f"{required}:latest" not in available_models:
                print(f"Error: Model '{required}' not found.")
                if required == SYNTHESIZER_MODEL:
                    print(f"Please create it first: ollama create {required} -f Modelfile_granite")
                else:
                    print(f"Please run: ollama pull {required}")
                sys.exit(1)
    except Exception as e:
        print(f"Error connecting to Ollama: {e}")
        print("Make sure Ollama is running and the 'ollama' python library is up to date.")
        sys.exit(1)

def run_research(query):
    print(f"\n[INFO] Starting research for: '{query}'")
    
    # --- AGENT 1: PLANNER ---
    print("Planner: Planning search queries...")
    planner_prompt = (
        f"Output exactly 3 optimized DuckDuckGo search strings for the query: '{query}'. "
        "Return ONLY a strict Python list of strings. No markdown, no commentary. "
        "Example: ['query 1', 'query 2', 'query 3']"
    )
    
    response = ollama.generate(model=PLANNER_MODEL, prompt=planner_prompt)
    try:
        search_queries = eval(response['response'].strip())
        if not isinstance(search_queries, list): raise ValueError
    except:
        print("⚠️ Planner output format failed. Attempting to clean...")
        # Fallback: try to find anything that looks like a list
        text = response['response']
        if "[" in text and "]" in text:
            search_queries = eval(text[text.find("["):text.find("]")+1])
        else:
            search_queries = [query] # Absolute fallback

    # --- SEARCH TOOL ---
    print(f"Search: Searching web for: {search_queries}...")
    aggregated_context = ""
    with DDGS() as ddgs:
        for q in search_queries:
            results = list(ddgs.text(q, max_results=3))
            for r in results:
                aggregated_context += f"Source: {r['href']}\nContent: {r['body']}\n\n"

    # --- AGENT 2: SYNTHESIZER ---
    print("Synthesizer: Synthesizing report...")
    synth_prompt = (
        f"Original Query: {query}\n\n"
        f"Search Context:\n{aggregated_context}\n\n"
        "Instructions: Based ONLY on the context above, write a comprehensive, well-structured Markdown report. "
        "Include sections like Executive Summary, Key Findings, and Detailed Analysis. Use citations if possible."
    )
    
    report_response = ollama.generate(model=SYNTHESIZER_MODEL, prompt=synth_prompt)
    report_content = report_response['response']

    # --- SAVE OUTPUT ---
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(report_content)
    
    print(f"Done: Research complete! Report saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    check_models()
    
    # HARDCODED QUERY FOR TESTING
    TEST_QUERY = "What are the latest updates on AI optimized laptops and PC?"
    
    run_research(TEST_QUERY)
