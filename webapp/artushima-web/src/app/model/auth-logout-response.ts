import { RequestStatus } from './request-status';
import { BlacklistedToken } from './blacklisted-token';

/**
 * The class representing the response body for the endpoint '/api/auth/logout'.
 */
export class AuthLogoutResponse {

  status: RequestStatus;
  message: string;
  token: BlacklistedToken;
}
