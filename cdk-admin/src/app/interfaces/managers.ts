export class ManagersInterface {
  id: number;
  name: string;
  surname: string;
  email: string;
  position: string;
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
