/**
 * The class representing the request body for the endpoint '/api/auth/login':
 */
export class AuthLoginRequest {

  userName: string;
  password: string;

  constructor(userName: string, password: string) {
    this.userName = userName;
    this.password = password;
  }
}
