export interface Place {
  id: number;
  name: string;
  address: string;
  category: string;
  rating: number | null;
  created_at: string;
}

export interface ApiError {
  detail: string;
}