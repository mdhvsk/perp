"use client"
import SearchSession from '@/components/search/SearchSession';
import { useParams } from 'next/navigation';
import React from 'react'


const SessionPage = () => {
    const params = useParams();
    const sessionId = params.id as string;
    return (
        <SearchSession id={sessionId}/>
    )
}

export default SessionPage