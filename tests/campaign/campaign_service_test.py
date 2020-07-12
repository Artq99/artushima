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
from artushima.user.persistence.model import UserEntity


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
        gm_id = 1
        gm_name = "Test game master"

        # when
        campaign_service.create_campaign(editor_name, campaign_name, begin_date, passed_days, gm_id, gm_name)

        # then
        self.campaign_repository_mock.persist.assert_called_once()
        campaign_entity: CampaignEntity = self.campaign_repository_mock.persist.call_args.args[0]
        self.assertEqual(campaign_name, campaign_entity.campaign_name)
        self.assertEqual(begin_date, campaign_entity.begin_date)
        self.assertEqual(passed_days, campaign_entity.passed_days)
        self.assertEqual(gm_id, campaign_entity.game_master_id)
        self.assertEqual(2, len(campaign_entity.campaign_history_entries))
        self.assertEqual(editor_name, campaign_entity.campaign_history_entries[0].editor_name)
        self.assertEqual(editor_name, campaign_entity.campaign_history_entries[1].editor_name)


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


class GetCampaignDetailsTest(TestCase):

    def setUp(self):
        self.campaign_repository_mock = create_autospec(campaign_repository)
        campaign_service.campaign_repository = self.campaign_repository_mock

    def tearDown(self):
        campaign_service.campaign_repository = campaign_repository

    def test_should_get_campaign_details(self):
        # given
        campaign = CampaignEntity()
        campaign.id = 99
        campaign.created_on = date(2020, 1, 1)
        campaign.modified_on = date(2020, 1, 1)
        campaign.opt_lock = 0
        campaign.campaign_name = "Test Campaign"
        campaign.begin_date = date(2055, 1, 1)
        campaign.passed_days = 10

        gm = UserEntity()
        gm.id = 88
        gm.created_on = date(2019, 1, 1)
        gm.modified_on = date(2019, 1, 1)
        gm.opt_lock = 0
        gm.user_name = "Test User"

        campaign.game_master = gm

        self.campaign_repository_mock.read_by_id.return_value = campaign

        # when
        campaign_details = campaign_service.get_campaign_details(99)

        # then
        self.assertEqual(99, campaign_details["id"])
        self.assertEqual("Test Campaign", campaign_details["title"])
        self.assertEqual(date(2020, 1, 1), campaign_details["creationDate"])
        self.assertEqual(date(2055, 1, 1), campaign_details["startDate"])
        self.assertEqual(10, campaign_details["passedDays"])
        self.assertEqual(date(2055, 1, 11), campaign_details["currentDate"])
        self.assertEqual(88, campaign_details["gameMasterId"])
        self.assertEqual("Test User", campaign_details["gameMasterName"])

    def test_should_get_business_error_when_campaign_id_is_none(self):
        # when then
        with self.assertRaises(BusinessError):
            campaign_service.get_campaign_details(None)

    def test_should_get_value_error_when_campaign_id_is_not_int(self):
        # when then
        with self.assertRaises(ValueError):
            campaign_service.get_campaign_details("1")

    def test_should_get_business_error_when_campaign_of_given_id_does_not_exist(self):
        # given
        self.campaign_repository_mock.read_by_id.return_value = None

        # when then
        with self.assertRaises(BusinessError):
            campaign_service.get_campaign_details(1)
