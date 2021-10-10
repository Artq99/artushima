/**
 * Configuration Class of the API URLs of the MyCampaigns module.
 *
 * @deprecated not intended for an outside use.
 */
class MyCampaignsURLs {
  endpoint: string;
  timelineEntry: string;
}

/**
 * Configuration class of the API URLs of the application.
 *
 * @deprecated not intended for an outside use.
 */
class ApiConfig {
  myCampaigns: MyCampaignsURLs;
}

/**
 * Configuration of the API URLs of the application.
 */
export const API_CONFIG = {
  myCampaigns: {
    endpoint: '/api/my_campaigns',
    timelineEntry: '/timeline/entry',
  } as MyCampaignsURLs,
} as ApiConfig;
