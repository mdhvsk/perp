from datetime import datetime
from typing import List, Dict, Any, Optional
from uuid import UUID
import logging
logger = logging.getLogger(__name__)

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
            response = self.supabase.table(self.table_name)\
                .select('*')\
                .eq('session_id', str(session_id))\
                .order('created_at', desc=False)\
                .execute()
            
            return response.data
        except Exception as e:
            raise Exception(f"Error fetching messages for session: {str(e)}")

    async def create_message(
        self,
        session_id: str,
        question: str,
        answer: str,
        sources: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new search message.
        
        Args:
            session_id (UUID): The session ID this message belongs to
            question (str): The search query or question asked
            answer (str): The response or answer to the question
            sources (List[Dict[str, Any]], optional): List of sources used for the answer
            
        Returns:
            Dict[str, Any]: The created message
        """
        try:
            message_data = {
                'session_id': str(session_id),
                'question': question,
                'answer': answer,
                'sources': sources or [],
                'created_at': datetime.utcnow().isoformat()
            }
            
            response = self.supabase.table(self.table_name)\
                .insert(message_data)\
                .execute()
            
            logging.info(response)
            
            return response.data[0]
        except Exception as e:
            raise Exception(f"Error creating message: {str(e)}")

    async def get_message_by_id(self, message_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific message by its ID.
        
        Args:
            message_id (UUID): The ID of the message to retrieve
            
        Returns:
            Optional[Dict[str, Any]]: The message if found, None otherwise
        """
        try:
            response = self.supabase.table(self.table_name)\
                .select('*')\
                .eq('id', str(message_id))\
                .limit(1)\
                .execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error fetching message: {str(e)}")

    async def update_message(
        self,
        message_id: UUID,
        answer: Optional[str] = None,
        sources: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Update an existing message's answer and/or sources.
        
        Args:
            message_id (UUID): The ID of the message to update
            answer (Optional[str]): New answer text
            sources (Optional[List[Dict[str, Any]]]): Updated list of sources
            
        Returns:
            Dict[str, Any]: The updated message
        """
        try:
            update_data = {}
            if answer is not None:
                update_data['answer'] = answer
            if sources is not None:
                update_data['sources'] = sources

            if not update_data:
                raise ValueError("No update parameters provided")

            response = self.supabase.table(self.table_name)\
                .update(update_data)\
                .eq('id', str(message_id))\
                .execute()
            
            return response.data[0]
        except Exception as e:
            raise Exception(f"Error updating message: {str(e)}")