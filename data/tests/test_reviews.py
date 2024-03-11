import server.endpoints as ep
import data.reviews as rvws
from http.client import (
    NOT_ACCEPTABLE,
    OK,
    SERVICE_UNAVAILABLE,
)
from unittest.mock import patch


TEST_CLIENT = ep.app.test_client()


def test_get_reviews():
    reviews = rvws.get_reviews()
    assert isinstance(reviews, dict)


@patch('data.reviews.add_review', return_value=rvws.MOCK_ID, autospec=True)
def test_review_add(mock_add):
    resp = TEST_CLIENT.post(ep.REVIEWS_EP, json=rvws.get_test_review())
    assert resp.status_code == OK


@patch('data.reviews.add_review', side_effect=ValueError(), autospec=True)
def test_review_bad_add(mock_add):
    """
    Testing we do the right thing with a value error from add_review.
    """
    resp = TEST_CLIENT.post(ep.REVIEWS_EP, json=rvws.get_test_review())
    assert resp.status_code == NOT_ACCEPTABLE


@patch('data.reviews.add_review', return_value=None)
def test_review_add_rvws_failure(mock_add):
    """
    Testing we do the right thing with a null ID return from add_review.
    """
    resp = TEST_CLIENT.post(ep.REVIEWS_EP, json=rvws.get_test_review())
    assert resp.status_code == SERVICE_UNAVAILABLE
