from datetime import date, datetime
from unittest import TestCase

from artushima.campaign import campaign_mapper
from artushima.campaign.persistence.model import CampaignTimelineEntity
from artushima.core.exceptions import DomainError
# Imported to prevent persistence errors
from artushima.user.persistence import model


class MapCreateTimelineEntryRequest(TestCase):

    def test_should_map_data_json(self):
        # given
        data_json = {
            "title": "Test",
            "sessionDate": "2050-01-01",
            "summaryText": "Test test test test test."
        }
        campaign_id = 1

        # when
        result = campaign_mapper.map_create_timeline_entry_request(data_json, campaign_id)

        # then
        self.assertEqual(result["title"], "Test")
        self.assertEqual(result["sessionDate"], date.fromisoformat("2050-01-01"))
        self.assertEqual(result["summaryText"], "Test test test test test.")
        self.assertEqual(result["campaignId"], 1)

    def test_should_map_data_json_when_summary_text_is_none(self):
        # given
        data_json = {
            "title": "Test",
            "sessionDate": "2050-01-01",
            "summaryText": None
        }
        campaign_id = 1

        # when
        result = campaign_mapper.map_create_timeline_entry_request(data_json, campaign_id)

        # then
        self.assertEqual(result["title"], "Test")
        self.assertEqual(result["sessionDate"], date.fromisoformat("2050-01-01"))
        self.assertEqual(result["summaryText"], None)
        self.assertEqual(result["campaignId"], 1)

    def test_should_map_data_json_when_summary_text_was_not_given(self):
        # given
        data_json = {
            "title": "Test",
            "sessionDate": "2050-01-01"
        }
        campaign_id = 1

        # when
        result = campaign_mapper.map_create_timeline_entry_request(data_json, campaign_id)

        # then
        self.assertEqual(result["title"], "Test")
        self.assertEqual(result["sessionDate"], date.fromisoformat("2050-01-01"))
        self.assertEqual(result["summaryText"], None)
        self.assertEqual(result["campaignId"], 1)

    def test_should_get_domain_error_when_data_is_none(self):
        # given
        campaign_id = 1

        # when then
        with self.assertRaises(DomainError):
            campaign_mapper.map_create_timeline_entry_request(None, campaign_id)

    def test_should_get_domain_error_when_title_was_not_given(self):
        # given
        data_json = {
            "sessionDate": "2050-01-01",
            "summaryText": "Test"
        }
        campaign_id = 1

        # when then
        with self.assertRaises(DomainError):
            campaign_mapper.map_create_timeline_entry_request(data_json, campaign_id)

    def test_should_get_domain_error_when_title_is_none(self):
        # given
        data_json = {
            "title": None,
            "sessionDate": "2050-01-01",
            "summaryText": "Test"
        }
        campaign_id = 1

        # when then
        with self.assertRaises(DomainError):
            campaign_mapper.map_create_timeline_entry_request(data_json, campaign_id)

    def test_should_get_value_error_when_title_is_invalid(self):
        # given
        data_json = {
            "title": 1,
            "sessionDate": "2050-01-01",
            "summaryText": "Test"
        }
        campaign_id = 1

        # when then
        with self.assertRaises(ValueError):
            campaign_mapper.map_create_timeline_entry_request(data_json, campaign_id)

    def test_should_get_domain_error_when_session_date_is_none(self):
        # given
        data_json = {
            "title": "Test",
            "sessionDate": None,
            "summaryText": "Test test test test test."
        }
        campaign_id = 1

        # when then
        with self.assertRaises(DomainError):
            campaign_mapper.map_create_timeline_entry_request(data_json, campaign_id)

    def test_should_get_domain_error_when_session_date_was_not_given(self):
        # given
        data_json = {
            "title": "Test",
            "summaryText": "Test test test test test.",
        }
        campaign_id = 1

        # when then
        with self.assertRaises(DomainError):
            campaign_mapper.map_create_timeline_entry_request(data_json, campaign_id)

    def test_should_get_value_error_when_session_date_is_invalid(self):
        # given
        data_json = {
            "title": "Test",
            "sessionDate": 1,
            "summaryText": "Test test test test test."
        }
        campaign_id = 1

        # when then
        with self.assertRaises(ValueError):
            campaign_mapper.map_create_timeline_entry_request(data_json, campaign_id)

    def test_should_get_domain_error_when_session_date_format_is_invalid(self):
        # given
        data_json = {
            "title": "Test",
            "sessionDate": "01.01.2050",
            "summaryText": "Test test test test test."
        }
        campaign_id = 1

        # when then
        with self.assertRaises(DomainError):
            campaign_mapper.map_create_timeline_entry_request(data_json, campaign_id)

    def test_should_get_value_error_when_summary_text_is_invalid(self):
        # given
        data_json = {
            "title": "Test",
            "sessionDate": "2050-01-01",
            "summaryText": 1
        }
        campaign_id = 1

        # when then
        with self.assertRaises(ValueError):
            campaign_mapper.map_create_timeline_entry_request(data_json, campaign_id)

    def test_should_get_domain_error_when_campaign_id_is_none(self):
        # given
        data_json = {
            "title": "Test",
            "sessionDate": "2050-01-01",
            "summaryText": "Test test test test test."
        }

        # when then
        with self.assertRaises(DomainError):
            campaign_mapper.map_create_timeline_entry_request(data_json, None)

    def test_should_get_value_error_when_campaign_id_is_invalid(self):
        # given
        data_json = {
            "title": "Test",
            "sessionDate": "2050-01-01",
            "summaryText": "Test test test test test."
        }

        # when then
        with self.assertRaises(ValueError):
            campaign_mapper.map_create_timeline_entry_request(data_json, list())


class MapTimelineEntryDataToTimelineEntity(TestCase):

    def test_should_map_data_to_entity(self):
        # given
        entry_data = {
            "title": "Test entry",
            "sessionDate": date.fromisoformat("2020-01-01"),
            "summaryText": "Test text.",
            "campaignId": 1
        }

        # when
        entity = campaign_mapper.map_timeline_entry_data_to_timeline_entity(entry_data)

        # then
        self.assertIsNone(entity.id)
        self.assertIsNotNone(entity.created_on)
        self.assertIsNotNone(entity.modified_on)
        self.assertEqual(entity.title, "Test entry")
        self.assertEqual(entity.session_date, date.fromisoformat("2020-01-01"))
        self.assertEqual(entity.summary_text, "Test text.")
        self.assertIsNone(entity.campaign_id)

    def test_should_map_data_to_entity_with_provided_timestamp(self):
        # given
        timestamp = datetime.fromisoformat("2005-01-01T10:00:00+00:00")
        entry_data = {
            "title": "Test entry",
            "sessionDate": date.fromisoformat("2020-01-01"),
            "summaryText": "Test text.",
            "campaignId": 1
        }

        # when
        entity = campaign_mapper.map_timeline_entry_data_to_timeline_entity(entry_data, timestamp)

        # then
        self.assertIsNone(entity.id)
        self.assertEqual(entity.created_on, timestamp)
        self.assertEqual(entity.modified_on, timestamp)
        self.assertEqual(entity.title, "Test entry")
        self.assertEqual(entity.session_date, date.fromisoformat("2020-01-01"))
        self.assertEqual(entity.summary_text, "Test text.")
        self.assertIsNone(entity.campaign_id)


class MapHistoryEntryDataToHistoryEntity(TestCase):

    def test_should_map_entry_data_to_entity(self):
        # given
        entry_data = {
            "editorName": "Test user",
            "message": "Test message."
        }

        # when
        entity = campaign_mapper.map_history_entry_data_to_history_entity(entry_data)

        # then
        self.assertIsNone(entity.id)
        self.assertIsNotNone(entity.created_on)
        self.assertIsNotNone(entity.modified_on)
        self.assertEqual(entity.opt_lock, 0)
        self.assertEqual(entity.editor_name, "Test user")
        self.assertEqual(entity.message, "Test message.")
        self.assertIsNone(entity.campaign_id)

    def test_should_map_entry_data_to_entity_with_provided_timestamp(self):
        # given
        timestamp = datetime.fromisoformat("2005-01-01T10:00:00+00:00")
        entry_data = {
            "editorName": "Test user",
            "message": "Test message."
        }

        # when
        entity = campaign_mapper.map_history_entry_data_to_history_entity(entry_data, timestamp)

        # then
        self.assertIsNone(entity.id)
        self.assertEqual(entity.created_on, timestamp)
        self.assertEqual(entity.modified_on, timestamp)
        self.assertEqual(entity.opt_lock, 0)
        self.assertEqual(entity.editor_name, "Test user")
        self.assertEqual(entity.message, "Test message.")
        self.assertIsNone(entity.campaign_id)


class MapCampaignTimelineEntityToDict(TestCase):

    def test_should_map_entity_to_dict(self):
        # given
        entity = CampaignTimelineEntity()
        entity.title = "Test title"
        entity.session_date = "2020-01-01"
        entity.summary_text = "Test text"

        # when
        data = campaign_mapper.map_campaign_timeline_entity_to_dict(entity)

        # then
        self.assertEqual("Test title", data["title"])
        self.assertEqual("2020-01-01", data["sessionDate"])
        self.assertEqual("Test text", data["summaryText"])
