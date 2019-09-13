/**
 * The request class for the endpoint '/api/auth/login':
 */
export class AuthTokenRequest {
  userName: string;
  password: string;

  constructor(userName: string, password: string) {
    this.userName = userName;
    this.password = password;
  }
}
