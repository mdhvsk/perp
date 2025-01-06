"use client"
import { dbService } from '@/services/db_service'
import { CreateMessageRequest, QueryGeneralRequest, Session } from '@/utils/types'
import { ChevronDown, MessageSquare, } from 'lucide-react'
import { useRouter } from 'next/navigation'
import React, { useEffect, useState } from 'react'
import SidebarComponent from './Sidebar'
import SearchBar from '../SearchBar'
import { CircleSpinner } from '../CircleSpinner'
import { queryService } from '@/services/query_service'
import { Button } from '@/components/ui/button'

const Dashboard = () => {
    const [sessions, setSessions] = useState<Session[]>([])
    const [loading, setLoading] = useState<boolean>(false)
    const [querying, setQuerying] = useState<boolean>(false)
    const router = useRouter()

    useEffect(() => {
        setLoading(true)
        const fetchSessions = async () => {
            const data = await dbService.getAllSessions()
            setSessions(data.reverse())
            setLoading(false)
        };
        fetchSessions();
    }, [])

    const getRelativeTimeString = (timestamp: string): string => {
        const now = new Date();
        const past = new Date(timestamp);
        const diffInMilliseconds = now.getTime() - past.getTime();
        const diffInMinutes = Math.floor(diffInMilliseconds / (1000 * 60));
        const diffInHours = Math.floor(diffInMilliseconds / (1000 * 60 * 60));
        const diffInDays = Math.floor(diffInMilliseconds / (1000 * 60 * 60 * 24));

        if (diffInMinutes < 60) {
            return `${diffInMinutes}m ago`;
        } else if (diffInHours < 24) {
            return `${diffInHours}h ago`;
        } else {
            return `${diffInDays}d ago`;
        }
    }

    const handleClickSession = (session_id: string) => {
        router.push(`/session/${session_id}`)
    }

    const handleSubmit = async (prompt: string) => {
        setQuerying(true)
        try {
            const new_session = await handleNewSession()
            if (new_session == null) return;
            await handleQuery(prompt, new_session.id)
            handleClickSession(new_session.id)
        } finally {
            setQuerying(false)
        }
    }

    const handleNewSession = async () => {
        const session = await dbService.createSession()
        if (session == null) return null
        return session
    }

    const handleQuery = async (prompt: string, session_id: string) => {
        const body: QueryGeneralRequest = { query: prompt }
        const message = await queryService.askHealthQuestion(body)
        console.log("*******Asking health question with sources**********")
        console.log(message)
        const messageBody: CreateMessageRequest = {
            session_id: session_id,
            question: prompt,
            answer: message.answer,
            sources: message.sources ? [{}] : []
        }
        await dbService.createMessage(messageBody)
    }

    return (
        <div className="flex h-screen bg-gray-50">
            <SidebarComponent />
            <div className="flex-1 flex flex-col">
                <div className="flex items-center justify-between p-4 border-b">
                </div>

                <div className="flex-1 overflow-auto px-4 py-8">
                    <div className="max-w-3xl mx-auto space-y-8">
                        {/* Welcome Section */}
                        <div className="text-center space-y-4">
                            <h2 className="text-4xl font-light text-gray-900">
                                Welcome to ChatAI
                            </h2>
                            <p className="text-gray-500">
                                Ask me anything about health and wellness
                            </p>
                        </div>

                        <SearchBar onSubmit={handleSubmit} loading={querying} />

                        {/* Recent Searches */}
                        <div className="space-y-4">
                            <div className="flex items-center justify-between">
                                <h3 className="text-lg font-medium text-gray-900 flex items-center gap-2">
                                    Recent conversations
                                    {loading && <CircleSpinner />}
                                </h3>
                                <Button variant="ghost" size="sm" className="text-gray-500">
                                    <ChevronDown className="w-4 h-4" />
                                    View all
                                </Button>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">


                                {sessions.slice(0, 6).map((session, index) => (
                                    <button
                                        key={index}
                                        onClick={() => handleClickSession(session.id)}
                                        className="h-32 p-4 bg-white border border-gray-200 rounded-lg hover:border-purple-400 transition-colors text-left group"
                                    >
                                        <div className="flex items-center gap-2 mb-2">
                                            <MessageSquare className="w-4 h-4 text-purple-600" />
                                            <span className="text-sm font-medium text-gray-900 group-hover:text-purple-600 truncate">
                                                {session.title}
                                            </span>
                                        </div>
                                        <p className="text-xs text-gray-500 mb-4 line-clamp-2">
                                            Click to continue your conversation...
                                        </p>
                                        <span className="text-xs text-gray-400">
                                            {getRelativeTimeString(session.updated_at)}
                                        </span>
                                    </button>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>

                <div className="p-4 border-t bg-white">
                    <div className="max-w-3xl mx-auto">
                        <div className="text-xs text-gray-500 text-center">
                            ChatAI has the potential to generate incorrect information.
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Dashboard