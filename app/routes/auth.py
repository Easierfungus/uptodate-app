from flask import Blueprint, request, jsonify
from app.services.supabase_service import supabase_client
from app.services.redis_service import redis_client
import logging

bp = Blueprint('auth', __name__, url_prefix='/api/auth')
logger = logging.getLogger(__name__)

@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        # Register with Supabase
        response = supabase_client.auth.sign_up({
            'email': email,
            'password': password
        })
        
        if response.user:
            # Cache session in Redis
            redis_client.setex(
                f"session:{response.user.id}",
                3600,
                response.session.access_token
            )
            
            return jsonify({
                'user': {'id': response.user.id, 'email': response.user.email},
                'access_token': response.session.access_token
            }), 201
        else:
            return jsonify({'error': 'Registration failed'}), 400
            
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        # Login with Supabase
        response = supabase_client.auth.sign_in_with_password({
            'email': email,
            'password': password
        })
        
        if response.user:
            # Cache session in Redis
            redis_client.setex(
                f"session:{response.user.id}",
                3600,
                response.session.access_token
            )
            
            return jsonify({
                'user': {'id': response.user.id, 'email': response.user.email},
                'access_token': response.session.access_token
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/logout', methods=['POST'])
def logout():
    try:
        # Get token from header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'No authorization header'}), 401
        
        # Sign out from Supabase
        supabase_client.auth.sign_out()
        
        return jsonify({'message': 'Logged out successfully'}), 200
        
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500