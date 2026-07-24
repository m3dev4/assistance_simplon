"use client"

import { apiInstance } from "@/services/api";
import { ChatRequest, ChatResponse } from "@/types/chat";
import { useMutation } from "@tanstack/react-query";

const sendQuestion = async (data: ChatRequest): Promise<ChatResponse> => {
  try {
    const response = await apiInstance.post("/chat/", data);
    return response.data;
  } catch (error) {
    console.error("Error sending question:", error);
    return { answer: "Une erreur s'est produite lors de l'envoi de la question." };
  }
};

export const useChat = () => {
  return useMutation({
    mutationKey: ["chat"],
    mutationFn: sendQuestion,
  });
};
