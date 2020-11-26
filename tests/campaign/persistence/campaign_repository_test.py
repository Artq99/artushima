"""
The test module for the campaign repository module.
"""

from datetime import date, datetime
from unittest import TestCase

from artushima.campaign.persistence import campaign_repository
from artushima.campaign.persistence.model import (CampaignEntity,
                                                  CampaignHistoryEntity,
                                                  CampaignTimelineEntity)
from artushima.core import db_access, properties
from artushima.core.exceptions import PersistenceError
from artushima.user.persistence.model import UserEntity


class PersistTest(TestCase):

    def setUp(self):
        properties.init()
        db_access.init()
        self.session = db_access.Session()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_should_persist_new_campaign(self):
        # given
        user = UserEntity()
        user.user_name = "test_user"
        user.created_on = datetime.utcnow()
        user.modified_on = datetime.utcnow()
        user.opt_lock = 0

        self.session.add(user)
        self.session.flush()

        new_campaign = CampaignEntity()
        new_campaign.created_on = datetime.utcnow()
        new_campaign.modified_on = datetime.utcnow()
        new_campaign.opt_lock = 0
        new_campaign.campaign_name = "test campaign"
        new_campaign.begin_date = date(2054, 1, 1)
        new_campaign.passed_days = 0
        new_campaign.game_master_id = user.id

        # when
        campaign_repository.persist(new_campaign)

        # then
        self.assertIn(new_campaign, self.session.query(CampaignEntity).all())

    def test_should_persist_new_campaign_with_history_entry(self):
        # given
        user = UserEntity()
        user.user_name = "test_user"
        user.created_on = datetime.utcnow()
        user.modified_on = datetime.utcnow()
        user.opt_lock = 0

        self.session.add(user)
        self.session.flush()

        new_campaign = CampaignEntity()
        new_campaign.created_on = datetime.utcnow()
        new_campaign.modified_on = datetime.utcnow()
        new_campaign.opt_lock = 0
        new_campaign.campaign_name = "test campaign"
        new_campaign.begin_date = date(2054, 1, 1)
        new_campaign.passed_days = 0
        new_campaign.game_master_id = user.id

        new_campaign_history_entry = CampaignHistoryEntity()
        new_campaign_history_entry.created_on = datetime.utcnow()
        new_campaign_history_entry.modified_on = datetime.utcnow()
        new_campaign_history_entry.opt_lock = 0
        new_campaign_history_entry.editor_name = "Test"
        new_campaign_history_entry.message = "Test message"
        new_campaign_history_entry.campaign = new_campaign

        # when
        campaign_repository.persist(new_campaign)

        # then
        self.assertIn(new_campaign, self.session.query(CampaignEntity).all())
        self.assertIsNotNone(self.session.query(CampaignHistoryEntity).filter_by(campaign_id=new_campaign.id).first())

    def test_should_persist_new_campaign_with_timeline_entry(self):
        # given
        user = UserEntity()
        user.user_name = "test_user"
        user.created_on = datetime.utcnow()
        user.modified_on = datetime.utcnow()
        user.opt_lock = 0

        self.session.add(user)
        self.session.flush()

        new_campaign = CampaignEntity()
        new_campaign.created_on = datetime.utcnow()
        new_campaign.modified_on = datetime.utcnow()
        new_campaign.opt_lock = 0
        new_campaign.campaign_name = "test campaign"
        new_campaign.begin_date = date(2054, 1, 1)
        new_campaign.passed_days = 0
        new_campaign.game_master_id = user.id

        new_campaign_timeline_entry = CampaignTimelineEntity()
        new_campaign_timeline_entry.created_on = datetime.utcnow()
        new_campaign_timeline_entry.modified_on = datetime.utcnow()
        new_campaign_timeline_entry.opt_lock = 0
        new_campaign_timeline_entry.title = "test session"
        new_campaign_timeline_entry.session_date = date.today()
        new_campaign_timeline_entry.summary_text = "this is summary"
        new_campaign_timeline_entry.campaign = new_campaign

        # when
        campaign_repository.persist(new_campaign)

        # then
        self.assertIn(new_campaign, self.session.query(CampaignEntity).all())
        self.assertIsNotNone(self.session.query(CampaignTimelineEntity).filter_by(campaign_id=new_campaign.id).first())

    def test_should_get_persistence_error_on_constraint_violation(self):
        # given
        new_campaign = CampaignEntity()

        # when then
        with self.assertRaises(PersistenceError):
            campaign_repository.persist(new_campaign)

    def test_should_raise_value_error_when_argument_is_of_wrong_type(self):
        # given
        new_campaign = str()

        # when then
        with self.assertRaises(ValueError):
            campaign_repository.persist(new_campaign)


class ReadByIdTest(TestCase):

    def setUp(self):
        properties.init()
        db_access.init()
        self.session = db_access.Session()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_should_get_campaign(self):
        # given
        user = UserEntity()
        user.user_name = "Test User"
        user.created_on = datetime.utcnow()
        user.modified_on = datetime.utcnow()
        user.opt_lock = 0

        campaign = CampaignEntity()
        campaign.campaign_name = "Test Campaign"
        campaign.created_on = datetime.utcnow()
        campaign.modified_on = datetime.utcnow()
        campaign.opt_lock = 0
        campaign.begin_date = date(2055, 1, 1)
        campaign.passed_days = 0
        campaign.game_master = user

        self.session.add(campaign)
        self.session.flush()

        # when
        found_campaign = campaign_repository.read_by_id(campaign.id)

        # then
        self.assertEqual(campaign, found_campaign)

    def test_should_get_none_when_campaign_does_not_exist(self):
        # when
        found_campaign = campaign_repository.read_by_id(999999)

        # then
        self.assertIsNone(found_campaign)


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
        user.created_on = datetime.utcnow()
        user.modified_on = datetime.utcnow()
        user.opt_lock = 0

        campaign_1 = CampaignEntity()
        campaign_1.campaign_name = "campaign_1"
        campaign_1.created_on = datetime.utcnow()
        campaign_1.modified_on = datetime.utcnow()
        campaign_1.opt_lock = 0
        campaign_1.begin_date = date(2055, 1, 1)
        campaign_1.passed_days = 0
        campaign_1.game_master = user

        campaign_2 = CampaignEntity()
        campaign_2.campaign_name = "campaign_2"
        campaign_2.created_on = datetime.utcnow()
        campaign_2.modified_on = datetime.utcnow()
        campaign_2.opt_lock = 0
        campaign_2.begin_date = date(2055, 1, 1)
        campaign_2.passed_days = 0
        campaign_2.game_master = user

        other_user = UserEntity()
        other_user.user_name = "other_user"
        other_user.created_on = datetime.utcnow()
        other_user.modified_on = datetime.utcnow()
        other_user.opt_lock = 0

        campaign_3 = CampaignEntity()
        campaign_3.campaign_name = "campaign_3"
        campaign_3.created_on = datetime.utcnow()
        campaign_3.modified_on = datetime.utcnow()
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
        user.created_on = datetime.utcnow()
        user.modified_on = datetime.utcnow()
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
