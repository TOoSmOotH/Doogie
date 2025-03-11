import apiClient from './client';
import chatService, { ChatWebSocket } from './chatService';
import documentService from './documentService';
import { userService, settingsService } from './userService';

// Export all API services
export {
  apiClient,
  chatService,
  ChatWebSocket,
  documentService,
  userService,
  settingsService,
};

// Export types
export type {
  // Chat types
  Chat,
  ChatMessage,
  MessageFeedback,
  ChatCreateRequest,
  MessageCreateRequest,
  FeedbackCreateRequest,
} from './chatService';

export type {
  // Document types
  Document,
  DocumentChunk,
  DocumentCreateRequest,
  DocumentUpdateRequest,
  DocumentUploadResponse,
  DocumentProcessResponse,
  SearchQuery,
  SearchResult,
} from './documentService';

export type {
  // User types
  User,
  UserSetting,
  SystemSetting,
  UserUpdateRequest,
  UserApprovalRequest,
  UserSettingUpdateRequest,
  SystemSettingCreateRequest,
  SystemSettingUpdateRequest,
} from './userService';

// Default export
export default {
  apiClient,
  chatService,
  documentService,
  userService,
  settingsService,
};