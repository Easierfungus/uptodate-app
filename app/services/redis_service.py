import os
import redis
import logging

logger = logging.getLogger(__name__)

def get_redis_client():
    """Get Redis client instance"""
    redis_url = os.environ.get('REDIS_URL')
    
    if not redis_url:
        raise ValueError("Redis URL must be set in environment variables")
    
    try:
        client = redis.from_url(redis_url, decode_responses=True)
        # Test connection
        client.ping()
        logger.info("Redis client initialized successfully")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Redis client: {str(e)}")
        raise

# Initialize client
redis_client = get_redis_client()