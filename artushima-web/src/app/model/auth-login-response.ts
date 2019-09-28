import { RequestStatus } from './request-status';
import { CurrentUser } from './current-user';

/**
 * The class representing the response body for the endpoint '/api/auth/login'.
 */
export class AuthLoginResponse {

  status: RequestStatus;
  message: string;
  currentUser: CurrentUser;
}
