import pytest
from datetime import datetime
from unittest.mock import patch
import json


from .coinbaseloader import CoinbaseLoader, Granularity


sample_pairs_response = json.dumps([
    {"id": "BTC-USD", "base_currency": "BTC", "quote_currency": "USD", "base_min_size": "0.001"},
    {"id": "ETH-USD", "base_currency": "ETH", "quote_currency": "USD", "base_min_size": "0.01"}
])

sample_stats_response = json.dumps({
    "id": "BTC-USD",
    "base_currency": "BTC",
    "quote_currency": "USD",
    "base_min_size": "0.001",
    "quote_increment": "0.01",
    "display_name": "BTC/USD"
})

sample_historical_data_response = json.dumps([
    [1625097600, 33513.57, 33687.53, 33600.00, 33653.99, 28.36152462],
    [1625011200, 33918.64, 33970.96, 33893.76, 33909.51, 27.52331336]
])

@pytest.fixture
def coinbase_loader():
    return CoinbaseLoader()

@patch.object(CoinbaseLoader, '_get_req')
def test_get_pairs(mock_get_req, coinbase_loader):
    mock_get_req.return_value = sample_pairs_response
    df = coinbase_loader.get_pairs()
    assert not df.empty
    assert "BTC-USD" in df.index
    assert df.loc["BTC-USD"]["base_currency"] == "BTC"
    assert df.loc["BTC-USD"]["quote_currency"] == "USD"

@patch.object(CoinbaseLoader, '_get_req')
def test_get_stats(mock_get_req, coinbase_loader):
    mock_get_req.return_value = sample_stats_response
    df = coinbase_loader.get_stats("BTC-USD")
    assert not df.empty
    assert df.loc[0, "id"] == "BTC-USD"
    assert df.loc[0, "base_currency"] == "BTC"
    assert df.loc[0, "quote_currency"] == "USD"

@patch.object(CoinbaseLoader, '_get_req')
@pytest.mark.parametrize("granularity", [Granularity.ONE_DAY, Granularity.ONE_HOUR])
def test_get_historical_data(mock_get_req, coinbase_loader, granularity):
    mock_get_req.return_value = sample_historical_data_response
    df = coinbase_loader.get_historical_data("BTC-USD", datetime(2021, 6, 30), datetime(2021, 7, 1), granularity)
    assert not df.empty
    assert "open" in df.columns
    assert "close" in df.columns
    assert df.index.name == "timestamp"
    assert df.iloc[0]["low"] == 33513.57
    assert df.iloc[0]["high"] == 33687.53

if __name__ == "__main__":
    pytest.main()
