"use client"
import { dbService } from '@/services/db_service'
import { CreateMessageRequest, QueryGeneralRequest, Session } from '@/utils/types'
import { useRouter } from 'next/navigation'
import React, { useEffect, useState } from 'react'
import SidebarComponent from './Sidebar'
import SearchBar from '../SearchBar'
import { queryService } from '@/services/query_service'
import WelcomeSection from './WelcomeSection'
import { RecentSessions } from './RecentSession'
import Footer from './Footer'

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
        await dbService.generateTitle({ "text": prompt, "session_id": session_id })
        const body: QueryGeneralRequest = { query: prompt }
        const message = await queryService.askHealthQuestion(body)
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
                <div className="flex items-center justify-between p-4 border-b" />

                <div className="flex-1 overflow-auto px-4 py-8">
                    <div className="max-w-3xl mx-auto space-y-8">
                        <WelcomeSection />
                        <SearchBar onSubmit={handleSubmit} loading={querying} />
                        <RecentSessions
                            sessions={sessions}
                            loading={loading}
                            onSessionClick={handleClickSession}
                            getRelativeTime={getRelativeTimeString}
                        />
                    </div>
                </div>

                <Footer />
            </div>
        </div>
    )
}

export default Dashboard