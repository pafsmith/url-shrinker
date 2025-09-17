from fastapi_limiter.depends import RateLimiter

rate_limit_dependency = RateLimiter(times=10, minutes=1)
