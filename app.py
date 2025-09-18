from flask import Flask, request, jsonify
from flask_cors import CORS
from EssayRating import workflow
import traceback
import os

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'UPSC Essay Rating API',
        'status': 'running',
        'endpoints': {
            'evaluate': '/evaluate (POST)',
            'health': '/health (GET)'
        }
    })

@app.route('/evaluate', methods=['POST'])
def evaluate_essay():
    try:
        # Check if Google API key is available
        if not os.getenv('GOOGLE_API_KEY'):
            return jsonify({'error': 'Google API key not configured'}), 500
            
        data = request.get_json()
        
        if not data or 'essay' not in data:
            return jsonify({'error': 'Essay text is required'}), 400
        
        essay_text = data['essay'].strip()
        
        if not essay_text:
            return jsonify({'error': 'Essay text cannot be empty'}), 400
        
        # Run the essay evaluation workflow
        initial_state = {
            'essay': essay_text
        }
        
        result = workflow.invoke(initial_state)
        
        # Format the response
        response = {
            'language_feedback': result.get('language_feedback', ''),
            'analysis_feedback': result.get('analysis_feedback', ''),
            'clarity_feedback': result.get('clarity_feedback', ''),
            'overall_feedback': str(result.get('overall_feedback', '')),
            'individual_score': result.get('individual_score', []),
            'avg_score': round(result.get('avg_score', 0), 2)
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error evaluating essay: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': 'Failed to evaluate essay. Please try again.'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'UPSC Essay Rating API is running'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
