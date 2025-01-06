import React, { useEffect, useRef, useState } from 'react';
import {  Search, SendHorizontal } from 'lucide-react';
import { CircleSpinner } from './CircleSpinner';
import { Button } from "@/components/ui/button";
import { Input } from './ui/input';

interface Props {
    onSubmit: (prompt: string) => void;
    loading: boolean
}

const SearchBar: React.FC<Props> = ({ onSubmit, loading}) => {
    const [formData, setFormData] = useState({
        prompt: '',
    });


    const handleSubmit = async () => {
        onSubmit(formData.prompt)
    }

    const messageRef = useRef<HTMLTextAreaElement>(null);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
        const { name, value } = e.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    

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
        <div className="w-full max-w-3xl mx-auto flex items-center gap-2 -z-50">
            <div className="flex-grow flex items-center relative bg-white rounded-full shadow-sm border border-gray-200">
                <div className="absolute left-4 text-gray-400">
                    <Search size={20} />
                </div>
                <Input
                    id="prompt"
                    name="prompt"
                    onChange={handleChange}
                    value={formData.prompt}
                    placeholder="Ask your health, nutrition, and fitness questions here"
                    className="border-0 focus-visible:ring-0 focus:outline-none text-gray-600 pl-12 pr-12 py-6 text-base placeholder:text-gray-400"
                />
                
            </div>
            <Button
                onClick={handleSubmit}
                size="icon"
                className="h-12 w-12 rounded-lg bg-[#7C3AED] hover:bg-[#6D28D9] text-white"
                disabled={loading}
            >
                {loading ? (
                    <CircleSpinner />
                ) : (
                    <SendHorizontal size={20} className="text-white" />
                )}
            </Button>
        </div>
    );
};

export default SearchBar;