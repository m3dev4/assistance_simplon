"use client";

import { useChat } from "@/hooks/useChat";
import { ArrowUp, Bot } from "lucide-react";
import { useState } from "react";

const ChatBot = () => {
  const [question, setQuestion] = useState("");
  const chat = useChat();

  const handleChat = () => {
    if (!question) {
      return;
    }
    chat.mutate({ question });
    setQuestion("");
  };

  return (
    <div className="min-h-screen w-screen overflow-hidden flex flex-col items-center justify-center">
      <h1 className="text-4xl font-bold text-left pt-7">Assistance Simplon</h1>
      <div className="fixed bottom-0 left-0 w-full h-44 flex items-center justify-center px-4">
        <div className="relative w-full max-w-5xl">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleChat();
              }
            }}
            placeholder="Écrivez votre message..."
            className="w-full border-2 p-4 pr-16 rounded-4xl focus:outline-none focus:border-blue-500 transition-colors"
          />
          <button
            aria-label="Envoyer"
            className="absolute right-4 top-1/2 -translate-y-1/2 bg-blue-500 text-white p-2 rounded-full hover:bg-blue-600 transition-colors duration-300"
            onClick={handleChat}
          >
            <ArrowUp />
          </button>
        </div>
      </div>
      <div className="flex flex-col w-full justify-self-start px-6 py-8">
        {chat.isPending && (
          <div className="flex items-center space-x-2">
            <Bot size={21} className="text-cyan-500" />
            <p>Reflexion...</p>
          </div>
        )}
        {chat.data && <p className="text-sm px-5">{chat.data.answer}</p>}
      </div>
    </div>
  );
};

export default ChatBot;
