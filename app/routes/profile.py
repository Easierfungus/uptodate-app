from flask import Blueprint, request, jsonify
from app.services.supabase_service import supabase_client
from app.services.redis_service import redis_client
import logging

bp = Blueprint('profile', __name__, url_prefix='/api/profile')
logger = logging.getLogger(__name__)

@bp.route('/', methods=['GET'])
def get_profile():
    try:
        # Get user from auth header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'No authorization header'}), 401
        
        token = auth_header.replace('Bearer ', '')
        
        # Get user from Supabase
        user = supabase_client.auth.get_user(token)
        
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        
        # Get profile from database
        response = supabase_client.table('profiles').select('*').eq('user_id', user.user.id).single().execute()
        
        if response.data:
            return jsonify(response.data), 200
        else:
            return jsonify({'error': 'Profile not found'}), 404
            
    except Exception as e:
        logger.error(f"Get profile error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/', methods=['POST'])
def create_profile():
    try:
        # Get user from auth header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'No authorization header'}), 401
        
        token = auth_header.replace('Bearer ', '')
        
        # Get user from Supabase
        user = supabase_client.auth.get_user(token)
        
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        
        data = request.get_json()
        profile_data = {
            'user_id': user.user.id,
            'name': data.get('name'),
            'bio': data.get('bio'),
            'age': data.get('age'),
            'location': data.get('location')
        }
        
        # Create profile in database
        response = supabase_client.table('profiles').insert(profile_data).execute()
        
        if response.data:
            # Cache profile in Redis
            redis_client.setex(
                f"profile:{user.user.id}",
                3600,
                str(response.data[0])
            )
            
            return jsonify(response.data[0]), 201
        else:
            return jsonify({'error': 'Failed to create profile'}), 400
            
    except Exception as e:
        logger.error(f"Create profile error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/selfie', methods=['POST'])
def upload_selfie():
    try:
        # Get user from auth header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'No authorization header'}), 401
        
        token = auth_header.replace('Bearer ', '')
        
        # Get user from Supabase
        user = supabase_client.auth.get_user(token)
        
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        
        # Check if selfie file is in request
        if 'selfie' not in request.files:
            return jsonify({'error': 'No selfie file provided'}), 400
        
        file = request.files['selfie']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Upload to Supabase Storage
        file_path = f"selfies/{user.user.id}/{file.filename}"
        
        response = supabase_client.storage.from_('selfies').upload(
            file_path,
            file.read(),
            {'content-type': file.content_type}
        )
        
        if response:
            # Get public URL
            public_url = supabase_client.storage.from_('selfies').get_public_url(file_path)
            
            # Update profile with selfie URL
            supabase_client.table('profiles').update({
                'selfie_url': public_url
            }).eq('user_id', user.user.id).execute()
            
            return jsonify({'selfie_url': public_url}), 200
        else:
            return jsonify({'error': 'Failed to upload selfie'}), 400
            
    except Exception as e:
        logger.error(f"Upload selfie error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500