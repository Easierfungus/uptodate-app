from flask import Blueprint, jsonify

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return jsonify({
        'app': 'Up to Date',
        'version': '1.0.0',
        'status': 'running'
    })

@bp.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200