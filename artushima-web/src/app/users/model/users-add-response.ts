import { RequestStatus } from 'src/app/core/model/request-status';

/**
 * The response of the API endpoint /api/users/add.
 */
export class UsersAddResponse {

  public status: RequestStatus;
  public message: string;
}
