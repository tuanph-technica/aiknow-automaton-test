import pytest
import softest
@pytest.mark.usefixtures("setup")
@pytest.mark.test_response_quality
class TestDocuments(softest.TestCase):
    @pytest.fixture(autouse=True)
    def class_setup(self, user_account):
        pass


