import { RequestStatus } from 'src/app/core/model/request-status';
import { MyCampaignsListElement } from './my-campaigns-list-element';

/**
 * The class for the response object of the endpoint /api/my_campaigns/list.
 */
export class MyCampaignsListResponse {
  public status: RequestStatus;
  public message: string;
  public myCampaigns: MyCampaignsListElement[];
}
