export class DeveloperInterface {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  hourly_rate: number;
  monthly_salary: number;
  birthday_date: Date;
  user: number;
  hours?: number;
  description?: string;
  developer?: number;
}

export class DeveloperListResponse {
  count: number;
  next: URL;
  previous: URL;
  results: Array<DeveloperInterface>
}
