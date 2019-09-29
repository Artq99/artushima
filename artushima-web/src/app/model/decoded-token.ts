import * as jwt_decode from 'jwt-decode';

/**
 * A class representing a decoded authentication token.
 */
export class DecodedToken {

  public sub: string;
  public iat: Date;
  public exp: Date;

  public constructor(token?: string) {

    if (token !== undefined) {
      let decoded = jwt_decode(token);

      this.sub = decoded.sub;
      this.iat = new Date(0);
      this.iat.setUTCSeconds(decoded.iat);
      this.exp = new Date(0);
      this.exp.setUTCSeconds(decoded.exp);
    }
  }
}
