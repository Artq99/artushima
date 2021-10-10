import { RequestStatus } from "./request-status";

/**
 * Base class for a response.
 */
export interface ResponseModel {
  message?: string;
  status?: RequestStatus;
}
