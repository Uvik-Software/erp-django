export class ManagersInterface {
  id: number;
  manager_name: string;
  manager_surname: string;
  manager_email: string;
  manager_position: string;
  address: string;
  company_name: string;
  user: number;
}

export class ManagersListResponse {
  count: number;
  next: URL;
  previous: URL;
  results: ManagersInterface[]
}
