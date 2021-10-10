import artushima.auth.persistence.model as auth_model
import artushima.campaign.persistence.model as campaign_model
import artushima.user.persistence.model as user_model


def assertModelInitialized():
    """
    Workarround for the problem with not initialized entities in Tests.

    If the problem occurs, just put this method in setUp.
    """

    assert auth_model is not None
    assert user_model is not None
    assert campaign_model is not None
