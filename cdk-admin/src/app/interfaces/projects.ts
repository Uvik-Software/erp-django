import { ClientInterface } from "./client";

export class ProjectTypes {
  value: string;
  name: string;
}

export class Currency {
  name: string;
}

export class ProjectInterface {
  id: number;
  project_name: string;
  project_type: "OUTSTAFF" | "FIX_PRICE_PROJECT" | "TIME_AND_MATERIAL";
  project_description: string;
  currency: string;
  basic_price: number;
  manager_info: string;
  client: ClientInterface;
  all_time_money_spent: number;
  deadline: Date;
  project_started_date: Date;
  owner: number;
}

export class getProjectsResponse {
  count: number;
  next: URL;
  previous: URL;
  results: ProjectInterface[]
}

export class devOnProject {
  description: string;
  developer: number;
  email: string;
  hourly_rate: number;
  hours: number;
  id: number;
  first_name: string;
  owner: number;
  project: number;
  project_name: string;
  last_name: string;
}

export class getAssignedDevs {
  count: number;
  next: URL;
  previous: URL;
  results: devOnProject[]
}
