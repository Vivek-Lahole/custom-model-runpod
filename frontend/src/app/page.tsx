"use client";

import {
  ChatBubble,
  ChatBubbleAvatar,
  ChatBubbleMessage,
} from "@/components/ui/chat/chat-bubble";
import { ChatInput } from "@/components/ui/chat/chat-input";
import { ChatMessageList } from "@/components/ui/chat/chat-message-list";
import { Button } from "@/components/ui/button";
import { CornerDownLeft, RefreshCw } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import useChat from "@/hooks/useChat";

interface ChatMessage {
  role: string;
  content: string;
}

export default function Home() {
  const [isGenerating, setIsGenerating] = useState(false);
  const [input, setInput] = useState("");
  const { ask, isLoading } = useChat();
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  const messagesRef = useRef<HTMLDivElement>(null);
  const formRef = useRef<HTMLFormElement>(null);

  useEffect(() => {
    if (messagesRef.current) {
      messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
    }
  }, [messages]);

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
  };

  const resetChat = () => {
    setMessages([]);
    setInput("");
    setIsGenerating(false);
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!input.trim() || isGenerating || isLoading) return;

    try {
      setIsGenerating(true);
      setMessages((prev) => [...prev, { role: "user", content: input }]);
      const response = await ask(input);
      setMessages((prev) => [...prev, response]);

      setInput("");
    } catch (error) {
      console.error("Failed to get response:", error);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (isGenerating || isLoading || !input.trim()) return;
      formRef.current?.requestSubmit();
    }
  };

  return (
    <main className="flex h-screen w-full max-w-3xl flex-col items-center mx-auto bg-muted/30 p-4 shadow-lg border border-gray-200 dark:border-gray-800 rounded-2xl m-3">
      <div className="flex justify-between items-center w-full border-b border-gray-200 dark:border-gray-800 py-4">
        <div className="flex items-center gap-3">
          <ChatBubbleAvatar src="/snoopy.jpg" fallback="SN" />
          <h1 className="text-2xl font-bold">Snoopy DOGG</h1>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="icon" onClick={resetChat}>
            <RefreshCw className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <div ref={messagesRef} className="flex-1 w-full overflow-y-auto py-6">
        <ChatMessageList>
          {messages.map((message, index) => (
            <ChatBubble
              key={index}
              variant={message.role === "user" ? "sent" : "received"}
            >
              <ChatBubbleAvatar
                src=""
                fallback={message.role === "user" ? "👨🏽" : "SN"}
              />
              <ChatBubbleMessage>{message.content}</ChatBubbleMessage>
            </ChatBubble>
          ))}

          {isGenerating && (
            <ChatBubble variant="received">
              <ChatBubbleAvatar src="/snoopy.jpg" fallback="SN" />
              <ChatBubbleMessage isLoading />
            </ChatBubble>
          )}
        </ChatMessageList>
      </div>

      <div className="w-full px-4 pb-4">
        <form
          ref={formRef}
          onSubmit={handleSubmit}
          className="relative rounded-lg border bg-background focus-within:ring-1 focus-within:ring-ring"
        >
          <ChatInput
            value={input}
            onKeyDown={handleKeyDown}
            onChange={handleInputChange}
            placeholder="Type your message here..."
            className="rounded-lg bg-background border-0 shadow-none focus-visible:ring-0"
          />
          <div className="flex items-center p-3 pt-0">
            <Button
              disabled={!input.trim() || isLoading}
              type="submit"
              size="sm"
              className="ml-auto gap-1.5"
            >
              Send Message
              <CornerDownLeft className="size-3.5" />
            </Button>
          </div>
        </form>
      </div>
    </main>
  );
}
