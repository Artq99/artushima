import { ResponseModel } from 'src/app/core/model/response.model';

/**
 * Model for the timeline entry editor.
 */
export interface TimelineEntryModel {
  title?: string;
  sessionDate?: string;
  summaryText?: string;
}

/**
 * Model for a response from an endpoint for timeline entry creation.
 */
export interface CreateTimelineEntryResponse extends ResponseModel {
  campaignTimelineEntryId?: number;
}
