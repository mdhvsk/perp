import { ChevronDown } from "lucide-react";
import { CircleSpinner } from "../CircleSpinner";
import { Button } from "../ui/button";
import { SessionCard } from "./SessionCard";
import { Session } from "@/utils/types";

interface RecentSessionsProps {
    sessions: Session[];
    loading: boolean;
    onSessionClick: (id: string) => void;
    getRelativeTime: (timestamp: string) => string;
}

export const RecentSessions: React.FC<RecentSessionsProps> = ({
    sessions,
    loading,
    onSessionClick,
    getRelativeTime
}) => (
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
                <SessionCard
                    key={index}
                    session={session}
                    onClick={onSessionClick}
                    getRelativeTime={getRelativeTime}
                />
            ))}
        </div>
    </div>
);
