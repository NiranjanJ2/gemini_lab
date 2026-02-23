"""
JSONPlaceholder API Client
Demonstrates REST API interactions with a free public API.
No API keys required - uses jsonplaceholder.typicode.com
"""
import requests as r
import requests
import json
import logging
from datetime import datetime
from typing import Dict, Optional, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Configuration - JSONPlaceholder is a free fake REST API
API_BASE_URL = "https://jsonplaceholder.typicode.com"
TIMEOUT = 30


class PostAPIClient:
    """Client for interacting with JSONPlaceholder posts API."""
    
    def __init__(self):
        """Initialize the API client."""
        self.session = r.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'PostClient/1.0'
        })
    
    def create_post(self, title: str, body: str, user_id: int = 1) -> Dict:
        """
        Create a new post.
        
        Args:
            title: Post title
            body: Post content
            user_id: ID of the user creating the post
            
        Returns:
            Dict containing post data including post_id
        """
        endpoint = f"{API_BASE_URL}/posts"
        payload = {
            'title': title,
            'body': body,
            'userId': user_id
        }
        
        try:
            logger.info(f"Creating post with title: {title}")
            response = r.post(endpoint, json=payload, timeout=TIMEOUT)
            response.raise_for_status()
            
            post_data = response.json()
            logger.info(f"Successfully created post: {post_data.get('id')}")
            return post_data
            
        except r.exceptions.RequestException as e:
            logger.error(f"Failed to create post: {str(e)}")
            raise
    
    def get_post(self, post_id: int) -> Optional[Dict]:
        """
        Retrieve post information by ID.
        
        Args:
            post_id: The unique identifier for the post
            
        Returns:
            Dict containing post data or None if not found
        """
        endpoint = f"{API_BASE_URL}/posts/{post_id}"
        
        try:
            logger.info(f"Fetching post data for ID: {post_id}")
            response = r.get(endpoint, timeout=TIMEOUT)
            
            if response.status_code == 404:
                logger.warning(f"Post not found: {post_id}")
                return None
                
            response.raise_for_status()
            return response.json()
            
        except r.exceptions.RequestException as e:
            logger.error(f"Failed to retrieve post: {str(e)}")
            raise
    
    def update_post(self, post_id: int, updates: Dict) -> Dict:
        """
        Update post information.
        
        Args:
            post_id: The unique identifier for the post
            updates: Dictionary of fields to update
            
        Returns:
            Dict containing updated post data
        """
        endpoint = f"{API_BASE_URL}/posts/{post_id}"
        
        try:
            logger.info(f"Updating post {post_id}")
            response = r.patch(endpoint, json=updates, timeout=TIMEOUT)
            response.raise_for_status()
            
            updated_post = response.json()
            logger.info(f"Successfully updated post: {post_id}")
            return updated_post
            
        except r.exceptions.RequestException as e:
            logger.error(f"Failed to update post: {str(e)}")
            raise
    
    def delete_post(self, post_id: int) -> bool:
        """
        Delete a post.
        
        Args:
            post_id: The unique identifier for the post
            
        Returns:
            True if deletion was successful
        """
        endpoint = f"{API_BASE_URL}/posts/{post_id}"
        
        try:
            logger.info(f"Deleting post {post_id}")
            response = r.delete(endpoint, timeout=TIMEOUT)
            response.raise_for_status()
            
            logger.info(f"Successfully deleted post: {post_id}")
            return True
            
        except r.exceptions.RequestException as e:
            logger.error(f"Failed to delete post: {str(e)}")
            raise
    
    def list_posts(self, limit: int = 10) -> List[Dict]:
        """
        Retrieve a list of posts.
        
        Args:
            limit: Number of posts to retrieve
            
        Returns:
            List of post dictionaries
        """
        endpoint = f"{API_BASE_URL}/posts"
        params = {'_limit': limit}
        
        try:
            logger.info(f"Fetching post list (limit {limit})")
            response = r.get(endpoint, params=params, timeout=TIMEOUT)
            response.raise_for_status()
            
            posts = response.json()
            logger.info(f"Retrieved {len(posts)} posts")
            return posts
            
        except r.exceptions.RequestException as e:
            logger.error(f"Failed to list posts: {str(e)}")
            raise
    
    def get_comments(self, post_id: int) -> List[Dict]:
        """
        Get all comments for a specific post.
        
        Args:
            post_id: The unique identifier for the post
            
        Returns:
            List of comment dictionaries
        """
        endpoint = f"{API_BASE_URL}/posts/{post_id}/comments"
        
        try:
            logger.info(f"Fetching comments for post {post_id}")
            response = r.get(endpoint, timeout=TIMEOUT)
            response.raise_for_status()
            
            comments = response.json()
            logger.info(f"Retrieved {len(comments)} comments")
            return comments
            
        except r.exceptions.RequestException as e:
            logger.error(f"Failed to get comments: {str(e)}")
            raise


def main():
    """Example usage of the PostAPIClient."""
    client = PostAPIClient()
    
    # Create a new post
    print("=== Creating a new post ===")
    new_post = client.create_post(
        title='My Test Post',
        body='This is the content of my test post.',
        user_id=1
    )
    print(f"Created post: {json.dumps(new_post, indent=2)}\n")
    
    # Retrieve post details
    print("=== Retrieving post details ===")
    post_id = 1
    post_details = client.get_post(post_id)
    print(f"Post details: {json.dumps(post_details, indent=2)}\n")
    
    # Update post
    print("=== Updating post ===")
    updates = {'title': 'Updated Title'}
    updated_post = client.update_post(post_id, updates)
    print(f"Updated post: {json.dumps(updated_post, indent=2)}\n")
    
    # List posts
    print("=== Listing posts ===")
    all_posts = client.list_posts(limit=5)
    print(f"Retrieved {len(all_posts)} posts\n")
    
    # Get comments
    print("=== Getting comments for post 1 ===")
    comments = client.get_comments(1)
    print(f"Retrieved {len(comments)} comments")
    print(f"First comment: {json.dumps(comments[0], indent=2)}")


if __name__ == '__main__':
    main()