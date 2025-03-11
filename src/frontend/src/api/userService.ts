import { get, post, put, del } from './client';

// Types
export interface User {
  id: string;
  email: string;
  full_name?: string;
  role: string;
  status: string;
}

export interface UserSetting {
  id: string;
  user_id: string;
  theme: string;
  default_llm_provider?: string;
  default_ollama_model?: string;
}

export interface SystemSetting {
  id: string;
  key: string;
  value: string;
  is_encrypted: boolean;
  created_at: string;
  updated_at: string;
}

export interface UserUpdateRequest {
  full_name?: string;
  role?: string;
  status?: string;
}

export interface UserApprovalRequest {
  approved: boolean;
}

export interface UserSettingUpdateRequest {
  theme?: string;
  default_llm_provider?: string;
  default_ollama_model?: string;
}

export interface SystemSettingCreateRequest {
  key: string;
  value: string;
  is_encrypted?: boolean;
}

export interface SystemSettingUpdateRequest {
  value?: string;
  is_encrypted?: boolean;
}

// User API services
export const userService = {
  // Get all users (admin only)
  getUsers: async (skip: number = 0, limit: number = 100): Promise<User[]> => {
    return get<User[]>('/users', { params: { skip, limit } });
  },

  // Get pending users (admin only)
  getPendingUsers: async (): Promise<User[]> => {
    return get<User[]>('/users/pending');
  },

  // Approve or reject a user (admin only)
  approveUser: async (userId: string, approval: UserApprovalRequest): Promise<User> => {
    return put<User>(`/users/approve/${userId}`, approval);
  },

  // Update a user (admin only)
  updateUser: async (userId: string, data: UserUpdateRequest): Promise<User> => {
    return put<User>(`/users/${userId}`, data);
  },

  // Delete a user (admin only)
  deleteUser: async (userId: string): Promise<void> => {
    return del<void>(`/users/${userId}`);
  },

  // Update current user
  updateCurrentUser: async (data: UserUpdateRequest): Promise<User> => {
    return put<User>('/users/me/update', data);
  },
};

// Settings API services
export const settingsService = {
  // Get user settings
  getUserSettings: async (): Promise<UserSetting> => {
    return get<UserSetting>('/settings/user');
  },

  // Update user settings
  updateUserSettings: async (data: UserSettingUpdateRequest): Promise<UserSetting> => {
    return put<UserSetting>('/settings/user', data);
  },

  // Get all system settings (admin only)
  getSystemSettings: async (): Promise<SystemSetting[]> => {
    return get<SystemSetting[]>('/settings/system');
  },

  // Get a specific system setting (admin only)
  getSystemSetting: async (key: string): Promise<SystemSetting> => {
    return get<SystemSetting>(`/settings/system/${key}`);
  },

  // Create a system setting (admin only)
  createSystemSetting: async (data: SystemSettingCreateRequest): Promise<SystemSetting> => {
    return post<SystemSetting>('/settings/system', data);
  },

  // Update a system setting (admin only)
  updateSystemSetting: async (
    key: string,
    data: SystemSettingUpdateRequest
  ): Promise<SystemSetting> => {
    return put<SystemSetting>(`/settings/system/${key}`, data);
  },

  // Delete a system setting (admin only)
  deleteSystemSetting: async (key: string): Promise<void> => {
    return del<void>(`/settings/system/${key}`);
  },
};

export default {
  userService,
  settingsService,
};