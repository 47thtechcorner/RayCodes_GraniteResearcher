# Perplexity-Lite: Local Multi-Agent Researcher

A highly focused, local-first research agent that searches the web and synthesizes comprehensive reports using Ollama models.

## 🚀 Tech Stack
- **Language:** Python
- **LLMs:** 
  - `gemma4:e2b` (Planner)
  - `granite4.1:3b` (Synthesizer - customized via Modelfile)
- **Search:** `duckduckgo-search` (DDGS)
- **Engine:** Ollama

## 🛠️ Setup Steps

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Pull Required Models:**
   ```bash
   ollama pull gemma4:e2b
   ollama pull granite4.1:3b
   ```

3. **Create Custom Granite Model:**
   This step is crucial to ensure the model provides direct outputs without internal monologue (`<think>` tags).
   ```bash
   ollama create granite-direct -f Modelfile_granite
   ```

## 🏃 Run Steps

1. **Configure Query:**
   Open `app.py` and modify the `TEST_QUERY` variable at the bottom.

2. **Execute Research:**
   ```bash
   python app.py
   ```

## 🧪 Test Steps
- Run the script with the default query: *"What are the latest updates on solid-state battery commercialization?"*
- Verify that `research_report.md` is generated in the project root.
- Check the terminal output to ensure the Planner generates 3 distinct queries and the Synthesizer processes the aggregated results.

## 📖 How it Works
1. **Planner (Agent 1):** Uses `gemma4:e2b` to take the user's query and break it down into 3 optimized search strings.
2. **Search Tool:** Uses `duckduckgo-search` to fetch the top 3 snippets for each of those queries, aggregating the text into a single context block.
3. **Synthesizer (Agent 2):** Uses a custom `granite-direct` model to process the context and original query, generating a structured Markdown report.
4. **Output:** The final report is saved to `research_report.md`.

## 🌟 Use Cases
- Market research and competitor analysis.
- Summarizing technical documentation or news.
- Rapid deep-dives into specific niche topics without browsing manually.

## 🔮 Future Ideas
- **Recursive Research:** Agents can ask follow-up questions if context is insufficient.
- **Source Citations:** Better parsing of URLs to provide inline citations.
- **UI Interface:** A simple Streamlit or FastAPI frontend.
- **Support for more models:** Dynamic model switching based on query complexity.
