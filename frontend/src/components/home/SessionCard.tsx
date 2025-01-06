import { Session } from "@/utils/types";
import { MessageSquare } from "lucide-react";

interface SessionCardProps {
    session: Session;
    onClick: (id: string) => void;
    getRelativeTime: (timestamp: string) => string;
}

export const SessionCard: React.FC<SessionCardProps> = ({ session, onClick, getRelativeTime }) => (
    <button
        onClick={() => onClick(session.id)}
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
            {getRelativeTime(session.updated_at)}
        </span>
    </button>
);