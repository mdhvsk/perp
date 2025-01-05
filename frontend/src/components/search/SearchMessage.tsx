import { Message } from '@/utils/types'
import { Copy, RotateCcw, Sparkles, ThumbsDown, ThumbsUp } from 'lucide-react'
import React, { useEffect, useState } from 'react'

interface Props {
  response: Message
  isNew: boolean
}

const SearchMessage: React.FC<Props> = ({ response, isNew }) => {
  const [displayedText, setDisplayedText] = useState('');
  const [isCopied, setIsCopied] = useState(false);
  const [currentIndex, setCurrentIndex] = useState(0);


  const [initials, setInitials] = useState(":)");
  const [charCount, setCharCount] = useState(0);
  const [wordCount, setWordCount] = useState(0);
  const [isLiked, setIsLiked] = useState(false);
  const [isDisliked, setIsDisliked] = useState(false);

  const updateCounts = (text: String) => {
    setCharCount(text.length);
    setWordCount(text.trim() === '' ? 0 : text.trim().split(/\s+/).length);
  };





  const isString = (value: unknown): value is string => {
    return typeof value === 'string';
  }

  const handleOnCopy = async () => {
    // try {
    //   if (isString(paragraph)) {
    //     await navigator.clipboard.writeText(paragraph);
    //     setIsCopied(true);
    //     setTimeout(() => {
    //       setIsCopied(false)
    //     }, 2000);

    //   }
    // } catch (e) {
    //   console.log(e);
    // }
  }

  const handleLiked = () => {
    setIsLiked(true)
    setTimeout(() => {
      setIsLiked(false);
    }, 1000)
  }
  const handleDisliked = () => {
    setIsDisliked(true)
    setTimeout(() => {
      setIsDisliked(false)
    }, 1000)
  }

  return (
    <>
      <div className="flex items-start space-x-3">
        <div className="w-8 h-8 bg-purple-600 rounded-full flex items-center justify-center flex-shrink-0">
          <span className="text-white font-semibold">{initials}</span>
        </div>
        <div className="bg-gray-800 rounded-lg p-3 flex-grow">

        </div>
      </div>

      <div className="flex items-start space-x-3">
        <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
          <Sparkles className="w-5 h-5 text-white" />
        </div>
        <div className="bg-gray-800 rounded-lg p-3 flex-grow">
          {/* {isParaphrased == "true" ? (<h2><strong>Paraphrase Results:</strong></h2>) : (<h2><strong>Academic Results:</strong></h2>)} */}
          <div className="mb-4">
            {displayedText}
            <span className="animate-pulse">|</span>
          </div>
        </div>
      </div>

      <div className="flex justify-between items-center text-gray-400 text-sm ">
        <div className="flex space-x-2">
          <button className="p-1 hover:bg-gray-700 rounded" onClick={handleOnCopy}><Copy className="w-4 h-4" /></button>
          <div className={"flex items-center text-xs rounded-md text-right text-gray-500"}>
            {wordCount} words | {charCount} chars
          </div>
        </div>

        <div className="flex space-x-2">
          
          <button className="p-1 hover:bg-gray-700 rounded"><ThumbsUp className="w-4 h-4" onClick={handleLiked} /></button>
          <button className="p-1 hover:bg-gray-700 rounded"><ThumbsDown className="w-4 h-4" onClick={handleDisliked} /></button>
        </div>
      </div>

      <div className="pb-8 flex justify-between items-center text-gray-400 text-sm ">
        <div className="flex space-x-2">
          {isCopied && (<p className='text-gray-500 animate-fade-in-out'>Copied!</p>)}
        </div>
        <div className="flex space-x-2">
          {isLiked && (<p className='text-gray-500 animate-fade-in-out'>Liked!</p>)}
          {isDisliked && (<p className='text-gray-500 animate-fade-in-out'>Disliked!</p>)}

        </div>
      </div>

    </>
  )
}

export default SearchMessage