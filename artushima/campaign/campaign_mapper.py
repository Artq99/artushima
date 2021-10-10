"""
Mapping methods for the campaign service.
"""

from datetime import datetime

from artushima.campaign.persistence.model import (CampaignHistoryEntity,
                                                  CampaignTimelineEntity)
from artushima.core.exceptions import DomainError
from artushima.core.utils.argument_validator import (assert_int, assert_str,
                                                     assert_str_or_none)
from artushima.core.utils.data_parser import parse_iso_date


def map_create_timeline_entry_request(data_json: dict, campaign_id: int) -> dict:
    """
    Map the input data of the request creating an entry in the campaign timeline.
    """

    if data_json is None:
        raise DomainError("Data not provided!", "D0000")

    title = data_json.get("title")
    session_date = data_json.get("sessionDate")
    summary_text = data_json.get("summaryText")

    assert_str(title, "DC003")
    assert_str(session_date, "DC004")
    assert_str_or_none(summary_text)
    assert_int(campaign_id, "DC001")

    parsed_session_date = parse_iso_date(session_date)

    return {
        "title": title,
        "sessionDate": parsed_session_date,
        "summaryText": summary_text,
        "campaignId": campaign_id
    }


def map_history_entry_data_to_history_entity(entry_data: dict, timestamp: datetime = None) -> CampaignHistoryEntity:
    """
    Map the data to an entry in a campaign history.
    """

    if timestamp is None:
        timestamp = datetime.utcnow()

    entity = CampaignHistoryEntity()
    entity.created_on = timestamp
    entity.modified_on = timestamp
    entity.opt_lock = 0
    entity.editor_name = entry_data["editorName"]
    entity.message = entry_data["message"]
    return entity


def map_timeline_entry_data_to_timeline_entity(entry_data: dict, timestamp: datetime = None) -> CampaignTimelineEntity:
    """
    Map the timeline entry data to a corresponding entity object.
    """

    if timestamp is None:
        timestamp = datetime.utcnow()

    entity = CampaignTimelineEntity()
    entity.created_on = timestamp
    entity.modified_on = timestamp
    entity.opt_lock = 0
    entity.title = entry_data["title"]
    entity.session_date = entry_data["sessionDate"]
    entity.summary_text = entry_data["summaryText"]
    return entity


def map_campaign_timeline_entity_to_dict(timeline_entity: CampaignTimelineEntity) -> dict:
    """
    Map the campaign timeline entity to a dictionary with data.
    """

    return {
        "title": timeline_entity.title,
        "sessionDate": timeline_entity.session_date,
        "summaryText": timeline_entity.summary_text,
    }
