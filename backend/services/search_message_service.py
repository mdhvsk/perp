from datetime import datetime
from typing import List, Dict, Any, Optional
from uuid import UUID

class SearchMessageService:
    def __init__(self, supabase_client):
        self.supabase = supabase_client
        self.table_name = 'search_messages'

    async def get_messages_by_session_id(self, session_id: UUID) -> List[Dict[str, Any]]:
        """
        Retrieve all messages for a specific session, ordered by creation time ascending.
        
        Args:
            session_id (UUID): The session ID to fetch messages for
            
        Returns:
            List[Dict[str, Any]]: List of messages ordered by created_at
        """
        try:
            response = await self.supabase.table(self.table_name)\
                .select('*')\
                .eq('session_id', str(session_id))\
                .order('created_at', desc=False)\
                .execute()
            
            return response.data
        except Exception as e:
            raise Exception(f"Error fetching messages for session: {str(e)}")

    async def create_message(
        self,
        session_id: UUID,
        role: str,
        message: str
    ) -> Dict[str, Any]:
        """
        Create a new message in a session.
        
        Args:
            session_id (UUID): The session ID this message belongs to
            role (str): The role of the message sender (e.g., 'user', 'assistant')
            message (str): The message content
            
        Returns:
            Dict[str, Any]: The created message
        """
        try:
            message_data = {
                'session_id': str(session_id),
                'role': role,
                'message': message,
                'created_at': datetime.utcnow().isoformat()
            }
            
            response = await self.supabase.table(self.table_name)\
                .insert(message_data)\
                .execute()
            
            return response.data[0]
        except Exception as e:
            raise Exception(f"Error creating message: {str(e)}")