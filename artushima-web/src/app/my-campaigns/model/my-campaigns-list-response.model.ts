import { RequestStatus } from 'src/app/core/model/request-status';

/**
 * The class for the data of a single campaign returned from the endpoint
 * /api/my_campaigns/list.
 */
export class MyCampaignsListElement {
  public id: number;
  public campaignName: string;
}

/**
 * The class representing the response body of the endpoint /api/my_campaigns/list.
 */
export class MyCampaignsListResponse {
  public status: RequestStatus;
  public message: string;
  public myCampaigns: MyCampaignsListElement[];
}
