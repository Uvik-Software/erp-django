export class Response {
  ok: boolean;
  message: string;
}

class DashboardReport {
  number_of_clients: number;
  number_of_developers: number;
  number_of_managers: number;
  number_of_projects: number
}

export class DashboardReportResponse extends Response {
  data: DashboardReport;
}
