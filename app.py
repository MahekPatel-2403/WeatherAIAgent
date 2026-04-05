
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchRun

from langchain_core.tools import tool
from concurrent import futures
import sys
import re
import utils
import requests
import os
from flask import Flask, render_template, request, jsonify


load_dotenv()

search_tool = DuckDuckGoSearchRun()


@tool
def get_weather_data(city: str) -> dict:
  """
  This function fetches the current weather data for a given city
  """
  url = f'https://api.weatherstack.com/current?access_key=4d1d8ae207a8c845a52df8a67bf3623e&query={city}'

  response = requests.get(url)

  return response.json()


def fetch_weather_data(city: str) -> dict:
    """Direct function to fetch weather (callable, not a tool)."""
    url = f"http://api.weatherapi.com/v1/current.json?key=eec49856ab1d48fcba661241263003&q={city}"
    response = requests.get(url, timeout=10)
    try:
        return response.json()
    except Exception:
        # Return raw text if JSON decode fails, useful for debugging API limits
        return {"success": False, "error": "invalid_response", "raw": response.text}


llm = HuggingFaceEndpoint(
    repo_id = "Qwen/Qwen2.5-7B-Instruct",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN"),
    task = "text-generation"
)
model = ChatHuggingFace(llm = llm)


def extract_place(query: str, search_text: str) -> str:
    """Try to extract a place name from the query or search result."""
    q = query.lower()
    # If user asked for a capital, try to extract it from search result
    if "capital of" in q or "capital" in q:
        m = re.search(r"capital[\s\w]*is\s+([A-Z][A-Za-z\s]+)", search_text)
        if m:
            return m.group(1).strip()
    # If user asked for weather "in <place>", extract from query
    m = re.search(r"in\s+([A-Za-z\s]+)$", query, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    # Try to find a capital-like phrase in the search result
    m = re.search(r"capital of .* is\s+([A-Z][A-Za-z\s]+)", search_text, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    # Fallback: take the last word of the query
    parts = query.split()
    if parts:
        return parts[-1].strip().strip(',')
    return "Bhopal"


def search_and_fetch(user_query: str) -> dict:
    """Perform search and fetch weather for the extracted place."""
    trace = []
    # Verbose logging to server console (no UI trace returned)
    print(f"[verbose] Received query: '{user_query}'")
    try:
        print(f"[verbose] Running search for '{user_query}'")
        search_result = search_tool.run(user_query)
        print(f"[verbose] Search result length: {len(str(search_result))}")
        trace.append({"type": "action", "title": "Searching", "detail": f"Search: {user_query}"})
    except Exception as e:
        search_result = f"Search failed: {e}"
        print(f"[verbose] Search error: {e}")

    search_text = search_result if isinstance(search_result, str) else str(search_result)
    print("[verbose] Extracting place from query and search result")
    place = extract_place(user_query, search_text)
    trace.append({"type": "observation", "title": "Place extracted", "detail": place})
    print(f"[verbose] Place extracted: {place}")

    print(f"[verbose] Fetching weather for '{place}'")
    weather = fetch_weather_data(place)
    print(f"[verbose] Weather response type: {type(weather)}")
    trace.append({"type": "result", "title": "Done", "detail": f"Results ready for {place}"})

    return {
        "query": user_query,
        "search": search_text,
        "place": place,
        "weather": weather,
        "trace": trace,
    }


app = Flask(__name__, static_folder='static', template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/query', methods=['POST'])
def api_query():
    data = request.get_json() or {}
    q = data.get('query', '').strip()
    if not q:
        return jsonify({'error': 'No query provided'}), 400
    result = search_and_fetch(q)
    return jsonify(result)


if __name__ == '__main__':
    # If run with command-line args, behave like before for quick tests
    if len(sys.argv) > 1:
        user_query = ' '.join(sys.argv[1:])
        out = search_and_fetch(user_query)
        print(out)
    else:
        app.run(host='127.0.0.1', port=7860, debug=True)