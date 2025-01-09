"use client";

import {
  ChatBubble,
  ChatBubbleAvatar,
  ChatBubbleMessage,
} from "@/components/ui/chat/chat-bubble";
import { ChatInput } from "@/components/ui/chat/chat-input";
import {
  ExpandableChat,
  ExpandableChatHeader,
  ExpandableChatBody,
  ExpandableChatFooter,
} from "@/components/ui/chat/expandable-chat";
import { ChatMessageList } from "@/components/ui/chat/chat-message-list";
import { Button } from "./ui/button";
import { Send } from "lucide-react";
import useChat from "@/hooks/useChat";
import { useEffect, useRef, useState } from "react";

interface ChatMessage {
  role: string;
  content: string;
}

export default function ChatSupport() {
  const [isGenerating, setIsGenerating] = useState(false);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const { ask, isLoading } = useChat();

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

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!input.trim() || isGenerating || isLoading) return;

    try {
      setIsGenerating(true);

      // Add user message
      setMessages((prev) => [...prev, { role: "user", content: input }]);

      // Get AI response with correct payload structure
      const response = await ask(input); // ask function now handles the payload structure
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
    <ExpandableChat size="md" position="bottom-right">
      <ExpandableChatHeader className="bg-muted/60 flex gap-2 items-center justify-start">
        <ChatBubbleAvatar src="/snoopy.jpg" fallback="SN" />
        <h1 className="text-xl font-semibold">Snoop Dogg</h1>
      </ExpandableChatHeader>
      <ExpandableChatBody>
        <ChatMessageList className="bg-muted/25">
          {/* Initial message */}
          <ChatBubble variant="received">
            <ChatBubbleAvatar src="/snoopy.jpg" fallback="SN" />
            <ChatBubbleMessage>Yo, what it do, baby boo? </ChatBubbleMessage>
          </ChatBubble>

          {/* Messages */}
          {messages.map((message, index) => (
            <ChatBubble
              key={index}
              variant={message.role === "user" ? "sent" : "received"}
            >
              <ChatBubbleAvatar
                src="/snoopy.jpg"
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
      </ExpandableChatBody>
      <ExpandableChatFooter className="bg-muted/25">
        <form
          ref={formRef}
          className="flex relative gap-2"
          onSubmit={handleSubmit}
        >
          <ChatInput
            value={input}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            className="min-h-12 bg-background shadow-none"
            placeholder="Type your message..."
          />
          <Button
            className="absolute top-1/2 right-2 transform -translate-y-1/2"
            type="submit"
            size="icon"
            disabled={isLoading || isGenerating || !input.trim()}
          >
            <Send className="size-4" />
          </Button>
        </form>
      </ExpandableChatFooter>
    </ExpandableChat>
  );
}
