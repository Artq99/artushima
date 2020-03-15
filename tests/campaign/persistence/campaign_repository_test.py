"""
The test module for the campaign repository module.
"""

from datetime import date, datetime
from unittest import TestCase

from artushima.campaign.persistence import campaign_repository
from artushima.campaign.persistence.model import CampaignEntity
from artushima.core import db_access, properties
from artushima.user.persistence.model import UserEntity


class ReadByGMNameTest(TestCase):

    def setUp(self):
        properties.init()
        db_access.init()
        self.session = db_access.Session()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_should_get_all_campaigns_of_given_gm(self):
        # given
        user = UserEntity()
        user.user_name = "test_user"
        user.created_on = datetime.now()
        user.modified_on = datetime.now()
        user.opt_lock = 0

        campaign_1 = CampaignEntity()
        campaign_1.campaign_name = "campaign_1"
        campaign_1.created_on = datetime.now()
        campaign_1.modified_on = datetime.now()
        campaign_1.opt_lock = 0
        campaign_1.begin_date = date(2055, 1, 1)
        campaign_1.passed_days = 0
        campaign_1.game_master = user

        campaign_2 = CampaignEntity()
        campaign_2.campaign_name = "campaign_2"
        campaign_2.created_on = datetime.now()
        campaign_2.modified_on = datetime.now()
        campaign_2.opt_lock = 0
        campaign_2.begin_date = date(2055, 1, 1)
        campaign_2.passed_days = 0
        campaign_2.game_master = user

        other_user = UserEntity()
        other_user.user_name = "other_user"
        other_user.created_on = datetime.now()
        other_user.modified_on = datetime.now()
        other_user.opt_lock = 0

        campaign_3 = CampaignEntity()
        campaign_3.campaign_name = "campaign_3"
        campaign_3.created_on = datetime.now()
        campaign_3.modified_on = datetime.now()
        campaign_3.opt_lock = 0
        campaign_3.begin_date = date(2055, 1, 1)
        campaign_3.passed_days = 0
        campaign_3.game_master = other_user

        self.session.add(campaign_1)
        self.session.add(campaign_2)
        self.session.add(campaign_3)
        self.session.flush()

        # when
        found_campaigns = campaign_repository.read_by_gm_id(user.id)

        # then
        self.assertIsNotNone(found_campaigns)
        self.assertIn(campaign_1, found_campaigns)
        self.assertIn(campaign_2, found_campaigns)
        self.assertNotIn(campaign_3, found_campaigns)

    def test_should_get_nothing_when_gm_has_no_campaigns(self):
        # given
        user = UserEntity()
        user.user_name = "test_user"
        user.created_on = datetime.now()
        user.modified_on = datetime.now()
        user.opt_lock = 0

        self.session.add(user)
        self.session.flush()

        # when
        found_campaigns = campaign_repository.read_by_gm_id(user.id)

        # then
        self.assertIsNotNone(found_campaigns)
        self.assertEqual(0, len(found_campaigns))

    def test_should_get_nothing_when_gm_does_not_exist(self):
        # when
        found_campaigns = campaign_repository.read_by_gm_id(9999)

        # then
        self.assertIsNotNone(found_campaigns)
        self.assertEqual(0, len(found_campaigns))
