import { IconDefinition } from '@fortawesome/fontawesome-common-types';
import { faFeatherAlt } from '@fortawesome/free-solid-svg-icons';

/**
 * Icon configuration class for the MyCampaigns module.
 *
 * @deprecated not intended for an outside use.
 */
class MyCampaignsIconConfig {
  timelineEntryEditorHeaderIcon: IconDefinition;
  campaignGmToolbarSummarizeSessionIcon: IconDefinition;
}

/**
 * Icon configuration class for the application.
 *
 * @deprecated not intended for an outside use.
 */
class IconConfig {
  myCampaigns: MyCampaignsIconConfig;
}

/**
 * Icon configuration constant for the application.
 */
export const APP_ICON_CONFIG = {
  myCampaigns: {
    timelineEntryEditorHeaderIcon: faFeatherAlt,
    campaignGmToolbarSummarizeSessionIcon: faFeatherAlt,
  } as MyCampaignsIconConfig,
} as IconConfig;
