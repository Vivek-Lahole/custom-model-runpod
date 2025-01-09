import backendRequest from "./BackendRequest";

interface ChatRequest {
  message: string;
  custom_dataset: boolean;
}

export default {
  chat: {
    ask(details: ChatRequest) {
      const path = "/chat";
      return backendRequest("POST", path, details);
    },
  },
};
