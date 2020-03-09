import { User } from './user';

/**
 * The response class for the endpoint /api/users/list.
 */
export class UsersListResponse {

  public status: string;
  public message: string;
  public users: User[];
}
