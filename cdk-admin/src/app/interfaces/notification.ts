export class Notification_ {
  id: number;
  title: string;
  description: string;
  type_notice: string;
  checked: boolean;
}

export class getAllNotifications {
  ok: boolean;
  message: string;
  results: Notification_[]
}
