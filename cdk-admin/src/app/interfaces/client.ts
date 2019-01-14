export class ClientInterface {
  id: number;
  first_name: string;
  last_name: string;
  username: string;
  position: string;
  company_name: string;
  address: string;
  email: string;
  phone: string;
  identification_number: number;
  owner: number;
}

export class ClientListResponse {
  count: number;
  next: URL;
  previous: URL;
  results: ClientInterface[]
}
