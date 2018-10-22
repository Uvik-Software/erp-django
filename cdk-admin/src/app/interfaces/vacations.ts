export class Vacation {
  id?: number;
  title: string;
  start: Date;
  end?: Date;
}


export class getVacationsResponse {
  ok: boolean;
  message: string;
  data: Vacation[]
}
