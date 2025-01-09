import { useCallback, useState } from "react";
import api from "../services/api";

export default function useChat() {
  const [isLoading, setIsLoading] = useState(false);

  const ask = useCallback(async (message: string) => {
    try {
      setIsLoading(true);
      const response = await api.chat.ask({
        message,
        custom_dataset: false,
      });
      return {
        role: "assistant",
        content: response.data.message,
      };
    } catch (error) {
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, []);

  return {
    isLoading,
    ask,
  };
}
