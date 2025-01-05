import React, { useEffect, useState } from 'react';
import SearchBar from '@/components/SearchBar';
import { CreateMessageRequest, Message, QueryGeneralRequest, Session } from '@/utils/types';
import { dbService } from '@/services/db_service';
import SidebarComponent from '../home/Sidebar';
import SearchMessage from './SearchMessage';
import { queryService } from '@/services/query_service';
import { Download, RotateCcw } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface SearchSessionProps {
    id: string;
}

const SearchSession: React.FC<SearchSessionProps> = ({ id }) => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [querying, setQuerying] = useState<boolean>(false);
    const [session, setSession] = useState<Session | null>(null);

    const retriveResponses = async (session_id: string) => {
        const responses = await dbService.getSessionMessages(session_id);
        if (responses == null) return;
        setMessages(responses);
    };

    const retriveSession = async (session_id: string) => {
        const session = await dbService.getSessionById(session_id);
        if (session == null) return null;
        setSession(session);
    };

    const handleSubmit = async (prompt: string) => {
        setQuerying(true);
        try {
            await handleQuery(prompt, id);
            await retriveResponses(id);
        } finally {
            setQuerying(false);
        }
    };

    const handleQuery = async (prompt: string, session_id: string) => {
        const body: QueryGeneralRequest = { query: prompt };
        const message = await queryService.searchGeneral(body);
        const messageBody: CreateMessageRequest = {
            session_id: session_id,
            question: prompt,
            answer: message.answer,
            sources: message.sources ? [{}] : [] // Fix for the 422 error
        };
        await dbService.createMessage(messageBody);
    };

    useEffect(() => {
        const session_id = String(id);
        retriveResponses(session_id);
        retriveSession(session_id);
    }, [id]);

    return (
        <div className="flex h-screen bg-gray-50">
            <SidebarComponent id={id}/>
            <div className="flex-1 flex flex-col">
                <div className="flex items-center justify-between p-4 border-b">
                    <h1 className="text-xl font-semibold text-gray-900">
                        {session?.title || "Chat"}
                    </h1>
                    <div className="flex gap-2">
                        <Button variant="ghost" className="text-gray-600">
                            <Download className="w-4 h-4 mr-2" />
                            Download chat
                        </Button>
                        <Button variant="ghost" className="text-gray-600">
                            <RotateCcw className="w-4 h-4 mr-2" />
                            Regenerate
                        </Button>
                    </div>
                </div>
                <div className="flex-1 overflow-auto px-4 py-2">
                    <div className="max-w-3xl mx-auto space-y-6">
                        {messages.map((message, index) => (
                            <SearchMessage 
                                key={index} 
                                response={message} 
                            />
                        ))}
                    </div>
                </div>
                <div className="p-4 border-t bg-white">
                    <div className="max-w-3xl mx-auto">
                        <SearchBar onSubmit={handleSubmit} loading={querying} />
                        <div className="text-xs text-gray-500 mt-2 text-center">
                            ChatAI has the potential to generate incorrect information.
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SearchSession;