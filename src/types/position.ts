import type { Detail } from './detail'


export interface Position {
  id: number;
  name: string;
  start_year: number;
  start_month: number;
  start_day: number;
  end_year?: number | null;
  end_month?: number | null;
  end_day?: number | null;
  salary?: number;
  details: Detail[];
}
