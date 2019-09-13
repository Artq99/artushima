import { CurrentUser } from './current-user';

/**
 * The response class for the endpoint '/api/auth/login'.
 */
export class AuthTokenResponse {

  status: string;
  message: string;
  currentUser: CurrentUser;
}
