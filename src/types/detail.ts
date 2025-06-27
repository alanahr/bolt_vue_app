import type { Entity } from './entity'

export interface Detail {
  id: number;
  name: string;
  description?: Record<string, any>;
  tags: Entity[];
  details: Detail[];
}