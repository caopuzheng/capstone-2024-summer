import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio

from ray.optimizer.portfolios import portfolio_performance
from ray.optimizer.strategies import max_sharpe, minimum_variance
from server.data_factory import cache_data
from server.data_model import Allocations, PortfolioSummary, StockInputs

LOCAL_REDIS_URL = "redis://localhost:6379/"

logger = logging.getLogger(__name__)
_data = cache_data(refresh_train=False, refresh_test=False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This specifies the startup and shutdown events for the FastAPI app.
    """
    HOST_URL = os.environ.get("REDIS_URL", LOCAL_REDIS_URL)
    logger.debug(HOST_URL)
    redis = asyncio.from_url(HOST_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    yield


app = FastAPI(
    lifespan=lifespan,
    swagger_ui_parameters={
        "syntaxHighlight.theme": "arta",
        "defaultModelExpandDepth": 1,
        "defaultModelRendering": "model",
    },
)


# app = FastAPI()

# @app.on_event("startup")
# async def startup():
#     HOST_URL = os.environ.get("REDIS_URL", LOCAL_REDIS_URL)
#     logger.info(f"Connecting to: {HOST_URL}")
#     redis = asyncio.from_url(HOST_URL)
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.post("/baseline_allocate")
@cache(expire=60)
async def baseline_allocate(stocks: StockInputs) -> Allocations:
    """
    Calibrates the allocation weights using the statistical methods.
    Return is cached for 60 seconds.
    """

    tickers = stocks.get_tickers()
    missing_tickers = [t for t in tickers if t not in _data.corr_matrix]
    if len(missing_tickers) > 0:
        raise ValueError(f"Tickers not found in the correlation matrix: {missing_tickers}")

    filtered_corr_matrix = _data.corr_matrix.loc[tickers, tickers]
    train = _data.train[tickers]
    test = _data.test[tickers]
    index = _data.test["SPY"]

    """
    TODO:
        - use the corralation matrix instead of training return
    """

    if stocks.risk_tolerance == "low":
        weights = minimum_variance(train, stocks.get_bounds())
    elif stocks.risk_tolerance == "high":
        weights = max_sharpe(train, stocks.get_bounds())
    elif stocks.risk_tolerance == "moderate":
        weight_1 = minimum_variance(train, stocks.get_bounds())
        weight_2 = max_sharpe(train, stocks.get_bounds())
        # take the average from these two list of weights
        weights = [(w1 + w2) / 2 for w1, w2 in zip(weight_1, weight_2)]

    port_weight_dict = {}
    port_weight_dict["baseline"] = weights

    # calcualte the portfolio performance using the test data and weights
    summeries = portfolio_performance(port_weight_dict, test, index)
    ticker_weights = {t: w for t, w in zip(tickers, weights)}

    return Allocations(ticker_weights=ticker_weights, summaries=summeries)


@app.post("/ml_allocate_cosine_similarity")
@cache(expire=60)
async def ml_allocate_cosine_similarity(stocks: StockInputs) -> Allocations:
    """
    Calibrates the allocation weights using ml-generated cosine similarity.
    Return is cached for 60 seconds.
    """

    weights = {h.ticker: 1 / len(stocks.stockList) for h in stocks.stockList}
    summeries = [
        PortfolioSummary(
            name="ml_cosine_similarity",
            mean_return=0.1,
            total_return=0.1,
            volatility=0.2,
            sharpe_ratio=0.5,
        ),
    ]

    return Allocations(ticker_weights=weights, summaries=summeries)


@app.get("/refresh_data")
@cache(expire=60)
async def refresh_data():
    """
    refresh the data from the s3 bucket and yahoo finance.
    """
    global _data
    _data = cache_data(refresh_train=True, refresh_test=True)

    return {f"message: Data refreshed. Newest test data: {_data.test.index.max()}"}


@app.get("/health")
async def health():
    """
    This endpoint returns the current date/time in ISO8601 format.
    """
    return {"time": datetime.now().isoformat()}


# @app.post("/ml_allocate_embeddings")
# @cache(expire=60)
# async def ml_allocate_embeddings(stocks: StockInputs) -> Allocations:
#     """
#     Calibrates the allocation weights using ml-generated embeddings.
#     Return is cached for 60 seconds.
#     """

#     weights = {h.ticker: 1 / len(stocks.stockList) for h in stocks.stockList}
#     summeries = [
#         PortfolioSummary(
#             name="baseline",
#             return_mean=0.1,
#             return_std=0.2,
#             sharpe_ratio=0.5,
#         ),
#         PortfolioSummary(
#             name="index",
#             return_mean=0.2,
#             return_std=0.4,
#             sharpe_ratio=0.5,
#         ),
#     ]

#     return Allocations(weights=weights, summaries=summeries)
