from flask import Blueprint, render_template, request, current_app, jsonify
import requests
import datetime
from urllib.parse import urlparse

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
        return jsonify({'error': 'No topic provided'}), 400

    topic = data['topic']
    current_date = datetime.date.today().isoformat()
    current_date_dmy = datetime.datetime.now().strftime('%d.%m.%Y')
    query = f"{topic} news {current_date_dmy}"
    
    # For demo purposes, return mock data
    mock_data = {
        "results": [
            {
                "title": f"Latest news about {topic}",
                "description": f"This is a sample description about {topic}.",
                "snippets": f"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed euismod, nisl nec ultricies lacinia, nisl nisl aliquam nisl, nec ultricies nisl nisl nec nisl. Sed euismod, nisl nec ultricies lacinia, nisl nisl aliquam nisl, nec ultricies nisl nisl nec nisl. Topics related to {topic} are trending today.",
                "url": "https://example.com/news/1",
                "source": "example.com"
            },
            {
                "title": f"Breaking: New developments in {topic}",
                "description": f"Recent updates about {topic} that you should know.",
                "snippets": f"Nunc euismod, nisl nec ultricies lacinia, nisl nisl aliquam nisl, nec ultricies nisl nisl nec nisl. Sed euismod, nisl nec ultricies lacinia, nisl nisl aliquam nisl, nec ultricies nisl nisl nec nisl. More information about {topic} is expected to be released soon.",
                "url": "https://example.com/news/2",
                "source": "example.com"
            },
            {
                "title": f"Analysis: What {topic} means for the future",
                "description": f"Experts weigh in on the implications of {topic}.",
                "snippets": f"Experts believe that {topic} will have significant impact on various sectors. According to Dr. Smith, '{topic} represents a paradigm shift in how we think about this area.' Others are more cautious, suggesting that more research is needed.",
                "url": "https://example.com/news/3",
                "source": "example.com"
            }
        ],
        "qnas": [
            {
                "question": f"What is the latest news about {topic}?",
                "answer": f"The latest news about {topic} involves new developments and research findings that suggest significant progress in this area."
            },
            {
                "question": f"Why is {topic} important?",
                "answer": f"{topic} is important because it affects multiple aspects of daily life and has implications for future technological and social developments."
            }
        ],
        "videos": [
            {
                "title": f"{topic} Explained",
                "description": f"A comprehensive explanation of {topic} and its implications.",
                "src": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            },
            {
                "title": f"The Future of {topic}",
                "description": f"Experts discuss what's next for {topic}.",
                "src": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            }
        ],
        "related": [
            f"{topic} trends",
            f"{topic} analysis",
            f"{topic} future",
            f"{topic} impact",
            f"{topic} research"
        ]
    }
    
    return jsonify(mock_data)