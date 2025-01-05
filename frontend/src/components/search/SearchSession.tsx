import React, { useEffect, useState } from 'react';
import router, { useRouter } from 'next/navigation';
import SearchBar from '@/components/SearchBar';
import { Message } from '@/utils/types';
import { dbService } from '@/services/db_service'
import HeaderComponent from '../home/Header';
import SidebarComponent from '../home/Sidebar';
import SearchMessage from './SearchMessage';

interface SearchSessionProps{
    id: string;
}

const SearchSession: React.FC<SearchSessionProps> = ({id}) => {
    const router = useRouter();
    const [responses, setResponses] = useState<Message[]>([]);
    const [summary, setSummary] = useState("")

    const populateResponses = (query: string, isPara: string, paragraph: string) => {
            // try {
            //     const query_response = new Message(query, isPara, paragraph);
            //     setResponses((prev) => [...prev, query_response]);
            // } catch (error) {
            //     console.error("Error creating QueryResponse:", error);
            // }
    
    }

    const postResponse = (query: string, isPara: string, paragraph: string) => {
            // populateResponses(query, isPara, paragraph)
            // insertResponse(Number(id), Boolean(isPara), paragraph, query)
    }

    const retriveResponses = async (session_id: string) => {
        let responses = await dbService.getSessionMessages(session_id)
        if (responses == null) return
        // for (let i = 0; i < responses.length; i++) {
        //     populateResponses(responses[i].prompt, String(responses[i].isParaphrased), responses[i].output)
        // }
    }

    const retriveEssay = async (essay_id: string) => {
        const essay = await dbService.getSessionById(essay_id)
        if (essay == null) return null
        // setSummary(essay[0].title)
    }

    useEffect(() => {
        let session_id = String(id);
        setResponses([])
        retriveResponses(session_id);
        retriveEssay(session_id);

    }, [id])

    return (
        <div className="bg-gray-900 text-white min-h-screen p-8">
            <HeaderComponent />
            <SidebarComponent/>                
            <div className="max-w-3xl mx-auto space-y-4">
                <strong className='text-2xl'>{summary}</strong>
                {responses.map((response, index) => (
                    <SearchMessage key={index} response={response} isNew={index === responses.length - 1}/>
                ))}
            </div>
            <SearchBar isHome={false} onResponse={postResponse} />


        </div>
    );
};

export default SearchSession;