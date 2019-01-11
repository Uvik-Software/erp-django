export class ManagersInterface {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  position: string;
  address: string;
  company_name: string;
}

export class ManagersListResponse {
  count: number;
  next: URL;
  previous: URL;
  results: ManagersInterface[]
}
