/**
 * The URL of the endpoint providing the list of the campaigns belonging
 * to the currently logged in game master.
 */
export const URL_MY_CAMPAIGNS_LIST = '/api/my_campaigns/list';

/**
 * The URL of the endpoint creating a new campaign with the currently
 * logged-in user as the game master.
 */
export const URL_MY_CAMPAIGNS_START = '/api/my_campaigns/start';

/**
 * The URL of the endpoint delivering the details of a campaign.
 */
export const URL_MY_CAMPAIGNS_DETAILS = '/api/my_campaigns/details';

/**
 * The default date for a campaign to begin with.
 * The date is the last date mentioned in the Neuroshima Handbook 1.5.
 */
export const DEFAULT_CAMPAIGN_START_DATE = '2053-11-18';
