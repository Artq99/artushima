import { RequestStatus } from 'src/app/core/model/request-status';

/**
 * The class for the response object of the endpoint /api/my_campaigns/start.
 */
export class MyCampaignsStartResponse {
  public status: RequestStatus;
  public message: string;
}
