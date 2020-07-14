import { Response } from 'src/app/shared/model/response.model';

/**
 * The response type for the endpoint \api\my_campaigns\details.
 */
export interface CampaignDetailsResponse extends Response {
  campaignDetails?: CampaignDetails;
}

/**
 * The type for details of a campaign.
 */
export interface CampaignDetails {
  id: number;
  title: string;
  creationDate: Date;
  startDate: Date;
  passedDays: number;
  currentDate: Date;
  gameMasterId: number;
  gameMasterName: string;
}
