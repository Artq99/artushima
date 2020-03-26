"""
The test module for the campaign service module.
"""

from datetime import date
from unittest import TestCase
from unittest.mock import create_autospec

from artushima.campaign import campaign_service
from artushima.campaign.persistence import campaign_repository
from artushima.campaign.persistence.model import CampaignEntity
from artushima.core.exceptions import BusinessError
from artushima.user import user_service


class CreateCampaignTest(TestCase):

    def setUp(self):
        self.campaign_repository_mock = create_autospec(campaign_repository)
        campaign_service.campaign_repository = self.campaign_repository_mock

    def tearDown(self):
        campaign_service.campaign_repository = campaign_repository

    def test_should_create_new_campaign(self):
        # given
        editor_name = "Test"
        campaign_name = "Test campaign"
        begin_date = date(2055, 1, 1)
        passed_days = 0
        game_master_id = 1

        # when
        campaign_service.create_campaign(editor_name, campaign_name, begin_date, passed_days, game_master_id)

        # then
        self.campaign_repository_mock.persist.assert_called_once()
        campaign_entity: CampaignEntity = self.campaign_repository_mock.persist.call_args.args[0]
        self.assertEqual(campaign_name, campaign_entity.campaign_name)
        self.assertEqual(begin_date, campaign_entity.begin_date)
        self.assertEqual(passed_days, campaign_entity.passed_days)
        self.assertEqual(game_master_id, campaign_entity.game_master_id)
        self.assertEqual(1, len(campaign_entity.campaign_history_entries))
        self.assertEqual(editor_name, campaign_entity.campaign_history_entries[0].editor_name)

    def test_should_get_exception_when_editor_name_is_none(self):
        # given
        editor_name = None
        campaign_name = "Test campaign"
        begin_date = date(2055, 1, 1)
        passed_days = 0
        game_master_id = 1

        # when then
        with self.assertRaises(ValueError):
            campaign_service.create_campaign(editor_name, campaign_name, begin_date, passed_days, game_master_id)

    def test_should_get_exception_when_editor_name_is_not_str(self):
        # given
        editor_name = 1
        campaign_name = "Test campaign"
        begin_date = date(2055, 1, 1)
        passed_days = 0
        game_master_id = 1

        # when then
        with self.assertRaises(TypeError):
            campaign_service.create_campaign(editor_name, campaign_name, begin_date, passed_days, game_master_id)

    def test_should_get_exception_when_editor_name_is_empty_str(self):
        # given
        editor_name = ""
        campaign_name = "Test campaign"
        begin_date = date(2055, 1, 1)
        passed_days = 0
        game_master_id = 1

        # when then
        with self.assertRaises(ValueError):
            campaign_service.create_campaign(editor_name, campaign_name, begin_date, passed_days, game_master_id)

    def test_should_get_exception_when_campaign_name_is_none(self):
        # given
        editor_name = "Test"
        campaign_name = None
        begin_date = date(2055, 1, 1)
        passed_days = 0
        game_master_id = 1

        # when then
        with self.assertRaises(ValueError):
            campaign_service.create_campaign(editor_name, campaign_name, begin_date, passed_days, game_master_id)

    def test_should_get_exception_when_campaign_name_is_not_str(self):
        # given
        editor_name = "Test"
        campaign_name = 1
        begin_date = date(2055, 1, 1)
        passed_days = 0
        game_master_id = 1

        # when then
        with self.assertRaises(TypeError):
            campaign_service.create_campaign(editor_name, campaign_name, begin_date, passed_days, game_master_id)

    def test_should_get_exception_when_campaign_name_is_empty_str(self):
        # given
        editor_name = "Test"
        campaign_name = ""
        begin_date = date(2055, 1, 1)
        passed_days = 0
        game_master_id = 1

        # when then
        with self.assertRaises(ValueError):
            campaign_service.create_campaign(editor_name, campaign_name, begin_date, passed_days, game_master_id)

    def test_should_get_exception_when_begin_date_is_none(self):
        # given
        editor_name = "Test"
        campaign_name = "Test campaign"
        begin_date = None
        passed_days = 0
        game_master_id = 1

        # when then
        with self.assertRaises(ValueError):
            campaign_service.create_campaign(editor_name, campaign_name, begin_date, passed_days, game_master_id)

    def test_should_get_exception_when_begin_date_is_not_date(self):
        # given
        editor_name = "Test"
        campaign_name = "Test campaign"
        begin_date = "01.01.2055"
        passed_days = 0
        game_master_id = 1

        # when then
        with self.assertRaises(TypeError):
            campaign_service.create_campaign(editor_name, campaign_name, begin_date, passed_days, game_master_id)

    def test_should_get_exception_when_passed_days_is_none(self):
        # given
        editor_name = "Test"
        campaign_name = "Test campaign"
        begin_date = date(2055, 1, 1)
        passed_days = None
        game_master_id = 1

        # when then
        with self.assertRaises(ValueError):
            campaign_service.create_campaign(editor_name, campaign_name, begin_date, passed_days, game_master_id)

    def test_should_get_exception_when_passed_days_is_not_int(self):
        # given
        editor_name = "Test"
        campaign_name = "Test campaign"
        begin_date = date(2055, 1, 1)
        passed_days = "0"
        game_master_id = 1

        # when then
        with self.assertRaises(TypeError):
            campaign_service.create_campaign(editor_name, campaign_name, begin_date, passed_days, game_master_id)

    def test_should_get_exception_when_game_master_id_is_none(self):
        # given
        editor_name = "Test"
        campaign_name = "Test campaign"
        begin_date = date(2055, 1, 1)
        passed_days = 0
        game_master_id = None

        # when then
        with self.assertRaises(ValueError):
            campaign_service.create_campaign(editor_name, campaign_name, begin_date, passed_days, game_master_id)

    def test_should_get_exception_when_game_master_id_is_not_int(self):
        # given
        editor_name = "Test"
        campaign_name = "Test campaign"
        begin_date = date(2055, 1, 1)
        passed_days = 0
        game_master_id = "1"

        # when then
        with self.assertRaises(TypeError):
            campaign_service.create_campaign(editor_name, campaign_name, begin_date, passed_days, game_master_id)


class GetCampaignsByGmIdTest(TestCase):

    def setUp(self):
        self.user_service_mock = create_autospec(user_service)
        self.campaign_repository_mock = create_autospec(campaign_repository)
        campaign_service.user_service = self.user_service_mock
        campaign_service.campaign_repository = self.campaign_repository_mock

    def tearDown(self):
        campaign_service.user_service = user_service
        campaign_service.campaign_repository = campaign_repository

    def test_should_get_campaigns(self):
        # given
        campaign = CampaignEntity()
        campaign.campaign_name = "campaign 1"
        campaign.begin_date = date(2055, 1, 1)
        campaign.passed_days = 10

        self.campaign_repository_mock.read_by_gm_id.return_value = [campaign]
        self.user_service_mock.get_user_by_user_name.return_value = {
            "id": 1,
            "user_name": "test_user"
        }

        # when
        campaigns = campaign_service.get_campaigns_by_gm_id(1)

        # then
        self.assertIsNotNone(campaigns)
        self.assertEqual(1, len(campaigns))
        self.assertEqual("campaign 1", campaigns[0]["campaign_name"])
        self.assertEqual(date(2055, 1, 1), campaigns[0]["begin_date"])
        self.assertEqual(10, campaigns[0]["passed_days"])

    def test_should_get_business_error_when_gm_id_is_none(self):
        # when then
        with self.assertRaises(BusinessError):
            campaign_service.get_campaigns_by_gm_id(None)

    def test_should_get_value_error_when_gm_id_is_not_int(self):
        # when then
        with self.assertRaises(ValueError):
            campaign_service.get_campaigns_by_gm_id("1")

    def test_should_get_business_error_when_gm_of_given_id_does_not_exist(self):
        # given
        self.user_service_mock.get_user_by_id.return_value = None

        # when then
        with self.assertRaises(BusinessError):
            campaign_service.get_campaigns_by_gm_id(1)
