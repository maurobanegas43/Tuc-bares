import type { Place } from './types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function fetchPlaces(limit: number = 10): Promise<Place[]> {
  const response = await fetch(`${API_URL}/places?limit=${limit}`, {
    signal: AbortSignal.timeout(5000)
  });
  
  if (!response.ok) {
    throw new Error(`Error: ${response.status}`);
  }
  
  return response.json();
}

export async function deleteAllPlaces(): Promise<{ deleted: number; message: string }> {
  const response = await fetch(`${API_URL}/places`, {
    method: 'DELETE',
    signal: AbortSignal.timeout(5000)
  });
  
  if (!response.ok) {
    throw new Error(`Error: ${response.status}`);
  }
  
  return response.json();
}

export async function deletePlace(placeId: number): Promise<{ deleted: number; message: string }> {
  const response = await fetch(`${API_URL}/places/${placeId}`, {
    method: 'DELETE',
    signal: AbortSignal.timeout(5000)
  });
  
  if (!response.ok) {
    throw new Error(`Error: ${response.status}`);
  }
  
  return response.json();
}

// ============================================
// CHAT - API de Gemini
// ============================================

export interface ChatResponse {
  answer: string;
  remaining?: number;
  limit_reached?: boolean;
  session_expires?: string;
}

export async function sendChat(message: string): Promise<ChatResponse> {
  const response = await fetch(`${API_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
    signal: AbortSignal.timeout(30000)
  });
  
  const data = await response.json();
  
  if (!response.ok) {
    throw new Error(data.detail || 'Error');
  }
  
  return data;
}

export interface ChatStatus {
  ip: string;
  messages_used: number;
  messages_remaining: number;
  max_messages: number;
  session_expires_hours: number;
  is_banned: boolean;
}

export async function getChatStatus(): Promise<ChatStatus> {
  const response = await fetch(`${API_URL}/chat/status`);
  return response.json();
}