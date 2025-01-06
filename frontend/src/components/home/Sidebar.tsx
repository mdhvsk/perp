import React, { useEffect, useState } from 'react';
import { CirclePlus, Search, FolderIcon, Star, Archive, Settings, HelpCircle, PanelLeftClose, PanelLeftOpen, MessageSquare, UserIcon } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Session } from '@/utils/types';
import { dbService } from '@/services/db_service';


interface SidebarProps {
    id?: string
}
const SidebarComponent: React.FC<SidebarProps> = ({id}) => {
    const [isOpen, setIsOpen] = useState(true);
    const [sessions, setSessions] = useState<Session[]>([])
    const router = useRouter()
    useEffect(() => {

        const fetchSessions = async () => {
            const data = await dbService.getAllSessions()
            setSessions(data.reverse())
            console.log(data)
        };
        fetchSessions();

    }, [])

    const handleNewChat = () => {
        router.push('/');
    };

    const handleGoToChat = (session_id: string) => {
        console.log("Going to session of id: " + session_id)
        router.push(`/session/${session_id}`)
    }

    const getRelativeTimeString = (timestamp: string): string => {
        const now = new Date();
        const past = new Date(timestamp);
        const diffInMilliseconds = now.getTime() - past.getTime();
        const diffInMinutes = Math.floor(diffInMilliseconds / (1000 * 60));
        const diffInHours = Math.floor(diffInMilliseconds / (1000 * 60 * 60));
        const diffInDays = Math.floor(diffInMilliseconds / (1000 * 60 * 60 * 24));

        if (diffInMinutes < 60) {
            return `${diffInMinutes} minute${diffInMinutes !== 1 ? 's' : ''} ago`;
        } else if (diffInHours < 24) {
            return `${diffInHours} hour${diffInHours !== 1 ? 's' : ''} ago`;
        } else {
            return `${diffInDays} day${diffInDays !== 1 ? 's' : ''} ago`;
        }
    }

    return (
        <div className='z-50'>
            <div className={`fixed top-0 left-0 h-full w-64 bg-white flex flex-col transition-transform duration-300 ease-in-out transform ${isOpen ? 'translate-x-0' : '-translate-x-full'}`}>
                <div className="p-4 space-y-4">
                    <Button
                        className="w-full justify-start gap-2 bg-[#7C3AED] hover:bg-[#6D28D9] text-white rounded-lg"
                        onClick={handleNewChat}
                    >
                        <CirclePlus size={20} />
                        New Chat
                    </Button>

                    <div className="relative">
                        <Search className="absolute left-3 top-2.5 h-4 w-4 text-gray-500" />
                        <Input
                            placeholder="Search"
                            className="pl-9 bg-gray-100 border-0 text-gray-900 placeholder:text-gray-500 rounded-lg"
                        />
                    </div>
                </div>

                <ScrollArea className="flex-1 px-4">
                    <div className="space-y-1">
                       

                        <Separator className="my-3" />

                        <div className="space-y-1">
                            {sessions.map((session, index) => (
                                <Button
                                    key={index}
                                    variant="ghost"

                                    onClick={() => handleGoToChat(session.id)} // Test with a simple console.log first

                                    className={`w-full justify-start gap-2 text-gray-700 hover:bg-gray-100 rounded-lg ${session.id === id ? 'bg-[#7C3AED]/10 text-[#7C3AED]' : ''}`}
                                >
                                    <MessageSquare size={16} />
                                    <div className="flex flex-col items-start">
                                        <span className="text-sm">{session.title}</span>
                                        <span className="text-xs text-gray-500">to provide you with more...</span>
                                    </div>
                                    <span className="ml-auto text-xs text-gray-500">{getRelativeTimeString(session.updated_at)}</span>
                                </Button>
                            ))}
                        </div>
                    </div>
                </ScrollArea>

                <div className="mt-auto p-4 border-t border-gray-200">
                    <Button
                        variant="ghost"
                        className="w-full justify-start gap-2 text-gray-700 hover:bg-gray-100 mb-2 rounded-lg"
                    >
                        <Settings size={16} />
                        <span>Settings</span>
                    </Button>
                    <Button
                        variant="ghost"
                        className="w-full justify-start gap-2 text-gray-700 hover:bg-gray-100 mb-4 rounded-lg"
                    >
                        <HelpCircle size={16} />
                        <span>Help</span>
                    </Button>

                    <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-full bg-gray-300 overflow-hidden">
                            <UserIcon width={32} height={32}/>
                        </div>
                        <div className="flex flex-col">
                            <span className="text-sm font-medium text-gray-900">Madhav Asok</span>
                            <span className="text-xs text-gray-500">Pro trial</span>
                        </div>
                        <Button
                            variant="outline"
                            size="icon"
                            className="fixed bottom-4 left-4 rounded-full z-50 bg-white hover:bg-gray-100 border-gray-200"
                            onClick={() => setIsOpen(false)}
                        >
                            <PanelLeftClose size={20} className="text-gray-700" />
                        </Button>
                    </div>
                </div>
            </div>

            {!isOpen && (
                <Button
                    variant="outline"
                    size="icon"
                    className="fixed bottom-4 left-4 rounded-full z-50 bg-white hover:bg-gray-100 border-gray-200"
                    onClick={() => setIsOpen(true)}
                >
                    <PanelLeftOpen size={20} className="text-gray-700" />
                </Button>
            )}
        </div>
    );
};

export default SidebarComponent;