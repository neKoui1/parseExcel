export interface ChatMessage {
  sender: string;
  content: string;
}

export type ChatDialog = {
  [dialogId: string]: Array<{ [role: string]: string }>;
};
