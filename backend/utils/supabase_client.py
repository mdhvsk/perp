import os
from typing import Optional
from supabase import create_client, Client
from dotenv import load_dotenv

class SupabaseClientSingleton:
    _instance: Optional['SupabaseClientSingleton'] = None
    _client: Optional[Client] = None
    
    def __init__(self) -> None:
        if SupabaseClientSingleton._instance is not None:
            raise RuntimeError("Use getInstance() instead")
            
        load_dotenv()  # Load environment variables
        
        supabase_url = os.getenv('NEXT_PUBLIC_SUPABASE_URL')
        supabase_key = os.getenv('NEXT_PUBLIC_SUPABASE_ANON_KEY')
        
        if not supabase_url or not supabase_key:
            raise ValueError('Missing Supabase environment variables')
            
        self._client = create_client(supabase_url, supabase_key)
        SupabaseClientSingleton._instance = self
        
    @classmethod
    def get_instance(cls) -> 'SupabaseClientSingleton':
        if cls._instance is None:
            cls._instance = SupabaseClientSingleton()
        return cls._instance
        
    def get_client(self) -> Client:
        if not self._client:
            raise RuntimeError('Supabase client is not initialized')
        return self._client

def get_supabase() -> Client:
    return SupabaseClientSingleton.get_instance().get_client()