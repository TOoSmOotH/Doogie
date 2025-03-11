import { get, post, put, del } from './client';

// Types
export interface Chat {
  id: string;
  title: string;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface ChatMessage {
  id: string;
  chat_id: string;
  role: string;
  content: string;
  thinking?: string;
  tokens?: number;
  created_at: string;
}

export interface MessageFeedback {
  id: string;
  message_id: string;
  feedback_type: 'positive' | 'negative' | 'neutral';
  comment?: string;
  created_at: string;
}

export interface ChatCreateRequest {
  title?: string;
}

export interface MessageCreateRequest {
  content: string;
}

export interface FeedbackCreateRequest {
  feedback_type: 'positive' | 'negative' | 'neutral';
  comment?: string;
}

// Chat API services
export const chatService = {
  // Get all chats
  getChats: async (): Promise<Chat[]> => {
    return get<Chat[]>('/chats');
  },

  // Get a specific chat
  getChat: async (chatId: string): Promise<Chat> => {
    return get<Chat>(`/chats/${chatId}`);
  },

  // Create a new chat
  createChat: async (data: ChatCreateRequest): Promise<Chat> => {
    return post<Chat>('/chats', data);
  },

  // Update a chat
  updateChat: async (chatId: string, data: ChatCreateRequest): Promise<Chat> => {
    return put<Chat>(`/chats/${chatId}`, data);
  },

  // Delete a chat
  deleteChat: async (chatId: string): Promise<void> => {
    return del<void>(`/chats/${chatId}`);
  },

  // Get messages for a chat
  getChatMessages: async (chatId: string): Promise<ChatMessage[]> => {
    return get<ChatMessage[]>(`/chats/${chatId}/messages`);
  },

  // Send a message to a chat (non-streaming)
  sendMessage: async (chatId: string, data: MessageCreateRequest): Promise<ChatMessage> => {
    return post<ChatMessage>(`/chats/${chatId}/messages`, data);
  },

  // Create feedback for a message
  createFeedback: async (
    chatId: string,
    messageId: string,
    data: FeedbackCreateRequest
  ): Promise<MessageFeedback> => {
    return post<MessageFeedback>(`/chats/${chatId}/messages/${messageId}/feedback`, data);
  },
};

// WebSocket for streaming chat
export class ChatWebSocket {
  private socket: WebSocket | null = null;
  private messageHandler: ((data: any) => void) | null = null;
  private errorHandler: ((error: Event) => void) | null = null;
  private closeHandler: ((event: CloseEvent) => void) | null = null;

  constructor(private chatId: string) {}

  // Connect to WebSocket
  connect(): void {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('Authentication token not found');
    }

    this.socket = new WebSocket(`${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}/api/chats/ws/${this.chatId}`);

    this.socket.onopen = () => {
      console.log('WebSocket connected');
    };

    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (this.messageHandler) {
        this.messageHandler(data);
      }
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error);
      if (this.errorHandler) {
        this.errorHandler(error);
      }
    };

    this.socket.onclose = (event) => {
      console.log('WebSocket closed:', event);
      if (this.closeHandler) {
        this.closeHandler(event);
      }
    };
  }

  // Send a message through WebSocket
  sendMessage(content: string): void {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
      throw new Error('WebSocket is not connected');
    }

    this.socket.send(JSON.stringify({ content }));
  }

  // Set message handler
  onMessage(handler: (data: any) => void): void {
    this.messageHandler = handler;
  }

  // Set error handler
  onError(handler: (error: Event) => void): void {
    this.errorHandler = handler;
  }

  // Set close handler
  onClose(handler: (event: CloseEvent) => void): void {
    this.closeHandler = handler;
  }

  // Disconnect WebSocket
  disconnect(): void {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }
}

export default chatService;