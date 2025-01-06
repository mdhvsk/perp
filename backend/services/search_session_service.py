from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

class SearchSessionService:
    def __init__(self, supabase_client):
        self.supabase = supabase_client
        self.table_name = 'search_sessions'

    async def get_all_sessions(self) -> List[Dict[str, Any]]:

        try:
            response = self.supabase.table(self.table_name)\
                .select('*')\
                .execute()
            
            # Return the data from the response
            return response.data
        except Exception as e:
            raise Exception(f"Error fetching search sessions: {str(e)}")

    async def get_session_by_id(self, session_id: UUID) -> Optional[Dict[str, Any]]:

        try:
            response = self.supabase.table(self.table_name)\
                .select('*')\
                .eq('id', str(session_id))\
                .limit(1)\
                .execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error fetching search session by ID: {str(e)}")

    async def create_session(self, title: str) -> Dict[str, Any]:

        try:
            current_time = datetime.utcnow().isoformat()
            session_data = {
                'title': title,
                'created_at': current_time,
                'updated_at': current_time
            }
            
            response = self.supabase.table(self.table_name)\
                .insert(session_data)\
                .execute()
            
            return response.data[0]
        except Exception as e:
            raise Exception(f"Error creating search session: {str(e)}")

    async def update_title(self, title: str, id: str) -> Dict[str, Any]:

        try:
          
            response = self.supabase.table(self.table_name)\
                .update({'title': title})\
                .eq('id', id)\
                .execute()
            
            return response
        except Exception as e:
            raise Exception(f"Error creating search session: {str(e)}")
    