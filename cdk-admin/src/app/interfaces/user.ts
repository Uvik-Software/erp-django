export type UserTypes = "MANAGER" | "DEVELOPER" | "CLIENT" | "JUST_CREATED";

export class User {
  date_joined: Date;
  username: string;
  email: string;
  first_name: string;
  groups: Array<string>;
  id: number;
  is_active: boolean;
  is_staff: boolean;
  is_superuser: boolean;
  last_login: Date;
  last_name: string;
  password: string;
  user_permissions: Array<string>;
  user_type: UserTypes;
}

export class getAllUsers {
  ok: boolean;
  message: string;
  data: User[]
}
