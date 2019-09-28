/**
 * The class for information of the currently logged in user.
 */
export class CurrentUser {

  userName: string;
  role: string; // TODO create enum for roles
  token: string;
}