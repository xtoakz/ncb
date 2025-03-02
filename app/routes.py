from flask import Blueprint, render_template, request, current_app, jsonify
import requests
import datetime
from urllib.parse import urlparse  # Zum Extrahieren des Domainnamens als Quelle
from supabase_client import supabase

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/imprint')
def imprint():
    return render_template('imprint.html')

@bp.route('/get_news', methods=['POST'])
def get_news():
    data = request.get_json()
    if not data or 'topic' not in data:
        return jsonify({'error': 'Kein Thema übermittelt'}), 400

    topic = data['topic']
    current_date = datetime.date.today().isoformat()  # Format: YYYY-MM-DD für die DB
    current_date_dmy = datetime.datetime.now().strftime('%d.%m.%Y')  # Für die API-Query
    query = f"{topic} Nachrichten {current_date_dmy}"
    
    params = {
        'api_key': current_app.config['RAGY_API'],
        'q': query,
        'lang': 'en',
        'country': 'US',
        'max_snippets_length': '10000'
    }
    
    response = requests.get("https://api.ragy.ai/v1/search", params=params)
    if response.status_code == 200:
        try:
            api_data = response.json()
        except ValueError:
            return jsonify({'error': 'Ungültige JSON-Antwort'}), 500
        
        if "results" in api_data:
            news_list = []
            for result in api_data["results"]:
                url_value = result.get("url", "")
                source = urlparse(url_value).netloc if url_value else ""
                news_data = {
                    "topic": topic,
                    "date": current_date,
                    "title": result.get("title", ""),
                    "description": result.get("description", ""),
                    "content": result.get("content", result.get("snippets", "")),
                    "url": url_value,
                    "source": source
                }
                news_list.append(news_data)
            if news_list:
                insert_response = supabase.table("news").upsert(news_list, on_conflict="url").execute()
                # Konvertiere die Response in ein Dictionary
                insert_response_dict = insert_response.dict()
                if insert_response_dict.get("error"):
                    return jsonify({"error": insert_response_dict["error"]["message"]}), 500
        
        return jsonify(api_data)
    else:
        return jsonify({'error': 'Fehler beim Abrufen der Nachrichten'}), response.status_code

