export class OwnerInterface {
  id: number;
  first_name: string;
  last_name: string;
  address: string;
  tax_number: string;
  num_contract_with_dev: number;
  date_contract_with_dev: Date;
}

export class getOwnersResponse {
  count: number;
  next: URL;
  previous: URL;
  results: OwnerInterface[]
}
