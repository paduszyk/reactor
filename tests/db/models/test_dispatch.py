from django.dispatch import Signal

from reactor.db.models.dispatch import connect_signals


def test_connect_signals_registers_model_method_as_signal_receiver():
    # Arrange.
    signal = Signal()

    class MockModel:
        class Meta:
            label_lower = "tests.mockmodel"

        _meta = Meta()

        signal_receivers = {
            "method": signal,
        }

        def method(self, **kwargs):
            pass

    # Act.
    connect_signals(MockModel)

    # Assert.
    assert signal.receivers[0][0][0] == "tests.mockmodel.method"

    # Clean up.
    signal.disconnect(dispatch_uid="tests.mockmodel.method")
