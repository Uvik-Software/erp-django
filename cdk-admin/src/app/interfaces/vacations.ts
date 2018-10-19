export class Vacation {
  title: string;
  start: Date;
  end?: Date;
}


export class getVacationsResponse {
  ok: boolean;
  message: string;
  data: Vacation[]
}
