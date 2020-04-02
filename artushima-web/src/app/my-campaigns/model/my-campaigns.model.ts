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
 * The class for the response object of the endpoint /api/my_campaigns/list.
 */
export class MyCampaignsListResponse {
  public status: RequestStatus;
  public message: string;
  public myCampaigns: MyCampaignsListElement[];
}

/**
 * The class for the request object of the endpoint /api/my_campaigns/start.
 */
export class MyCampaignsStartRequest {
  public campaignName: string;
  public beginDate: string;
}

/**
 * The class for the response object of the endpoint /api/my_campaigns/start.
 */
export class MyCampaignsStartResponse {
  public status: RequestStatus;
  public message: string;
}
