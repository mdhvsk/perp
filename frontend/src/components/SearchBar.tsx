import React, { FormEvent, useEffect, useRef, useState } from 'react';
import { Camera, Mic, Search, SendHorizontal } from 'lucide-react';
import { CircleSpinner } from './CircleSpinner';
import { useRouter } from 'next/navigation';
import { Button } from "@/components/ui/button";
import { Input } from './ui/input';
import { dbService } from '@/services/db_service';

interface Props {
    isHome: boolean;
    onResponse: (prompt: string, isParaphrase: string, paragraph: string) => void;
    onQuery: (prompt: string) => void;
    onSubmit: (prompt: string) => void;
}

const SearchBar: React.FC<Props> = ({ isHome, onResponse, onSubmit }) => {
    const [formData, setFormData] = useState({
        prompt: '',
    });


    const messageRef = useRef<HTMLTextAreaElement>(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
        const { name, value } = e.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    


    const handleNewSession = async () => {
        const session = await dbService.createSession()
        if(session == null) return

        
    }

    useEffect(() => {
        adjustTextareaHeight();
    }, [formData.prompt]);

    const adjustTextareaHeight = () => {
        const textarea = messageRef.current;
        if (textarea) {
            textarea.style.height = 'auto';
            textarea.style.height = `${textarea.scrollHeight}px`;
        }
    };

    return (
        <div className="w-full max-w-3xl mx-auto flex items-center gap-2">
            <div className="flex-grow flex items-center relative bg-white rounded-full shadow-sm border border-gray-200">
                <div className="absolute left-4 text-gray-400">
                    <Camera size={20} />
                </div>
                <Input
                    id="prompt"
                    name="prompt"
                    onChange={handleChange}
                    value={formData.prompt}
                    placeholder="Enter a prompt here..."
                    className="border-0 focus-visible:ring-0 focus:outline-none text-gray-600 pl-12 pr-12 py-6 text-base placeholder:text-gray-400"
                />
                <div className="absolute right-4 text-gray-400">
                    <Mic size={20} />
                </div>
            </div>
            <Button
                onClick={() => onSubmit}
                size="icon"
                className="h-12 w-12 rounded-lg bg-[#7C3AED] hover:bg-[#6D28D9] text-white"
                disabled={isLoading}
            >
                {isLoading ? (
                    <CircleSpinner />
                ) : (
                    <SendHorizontal size={20} className="text-white" />
                )}
            </Button>
        </div>
    );
};

export default SearchBar;