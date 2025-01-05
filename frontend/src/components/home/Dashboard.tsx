"use client"
import { dbService } from '@/services/db_service'
import { Session } from '@/utils/types'
import { ChevronDown } from 'lucide-react'
import { useRouter } from 'next/navigation'
import React, { useEffect, useState } from 'react'
import HeaderComponent from './Header'
import SidebarComponent from './Sidebar'
import SearchBar from '../SearchBar'
import { CircleSpinner } from '../CircleSpinner'

type Props = {}

const Dashboard = (props: Props) => {
    const [sessions, setSessions] = useState<Session[]>([])
    const [loading, setLoading] = useState<boolean>(false)
    const router = useRouter()
    useEffect(() => {
        setLoading(true)

        const fetchSessions = async () => {
            const user_id = Number(localStorage.getItem('id'))
            const data = await dbService.getAllSessions()
            setSessions(data)
            setLoading(false)
            console.log(data)
        };
        fetchSessions();

    }, [])

    const getRelativeTimeString = (timestamp: string): string  =>{
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

    const handleClickSession = (session_id: string) => {
        router.push(`/session/${session_id}`)
    }

    return (
        <div className="bg-gray-900 text-gray-200 min-h-screen p-8">
            <HeaderComponent />
            <SidebarComponent />
            <h2 className="text-4xl font-light mb-8 flex justify-center">
                Hi !
            </h2>
            <SearchBar isHome={true} onResponse={() => { }} />

            <div className="max-w-3xl mx-auto space-y-2 my-4">
                <h3 className="flex items-center text-lg mb-4">
                    Your recent searches
                    <ChevronDown size={16} className="ml-2 mr-8" />
                    {loading && <CircleSpinner />}

                </h3>
                <div className="grid grid-cols-3 gap-4">
                    {sessions.slice(0, 6).map((session, index) => (
                        <button key={index} className="bg-gray-800 p-4 rounded-lg hover:bg-gray-600" onClick={() => handleClickSession(session.id)}>
                            <h4 className="font-medium mb-2">{session.title}</h4>
                            <p className="text-sm text-gray-400">{getRelativeTimeString(session.updated_at)}</p>
                        </button>
                    ))}

                </div>
            </div>

        </div>)
}

export default Dashboard