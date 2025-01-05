import { Message } from '@/utils/types';
import { Copy, MessageSquare, ThumbsDown, ThumbsUp, UserIcon } from 'lucide-react';
import Image from 'next/image';
import React, { useState } from 'react';

interface Props {
  response: Message;
  isNew: boolean;
}

const SearchMessage: React.FC<Props> = ({ response, isNew }) => {
  const [isCopied, setIsCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(response.answer);
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 2000);
    } catch (error) {
      console.error('Failed to copy:', error);
    }
  };

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
    <div className="space-y-4">
      {/* User message */}
      <div className="flex gap-4 items-start bg-gray-50 p-4 rounded-lg">
        <div className="w-8 h-8 rounded-full bg-blue-100 flex-shrink-0 flex items-center justify-center">
          <UserIcon className="w-5 h-5 text-blue-600" />
        </div>
        <div className="flex-1">
          <div className="text-sm text-gray-500 mb-1">You · 15m</div>
          <div className="text-gray-900">{response.question}</div>
        </div>
        <button className="text-gray-400 hover:text-gray-600">
          <Copy className="w-4 h-4" />
        </button>
      </div>

      {/* AI response */}
      <div className="flex gap-4 items-start bg-white p-4 rounded-lg shadow-sm border border-gray-100">
        <div className="w-8 h-8 rounded-full bg-purple-100 flex-shrink-0 flex items-center justify-center">
          <MessageSquare className="w-5 h-5 text-purple-600" />
        </div>
        <div className="flex-1">
          <div className="text-sm text-gray-500 mb-1">ChatAI · 15m</div>
          <div className="text-gray-900 whitespace-pre-wrap">{response.answer}</div>
        </div>
        <div className="flex gap-2">
          <button
            className={`text-gray-400 hover:text-gray-600 ${isCopied ? 'text-green-500' : ''}`}
            onClick={handleCopy}
          >
            <Copy className="w-4 h-4" />
          </button>
          <button className="text-gray-400 hover:text-gray-600">
            <ThumbsUp className="w-4 h-4" />
          </button>
          <button className="text-gray-400 hover:text-gray-600">
            <ThumbsDown className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default SearchMessage;