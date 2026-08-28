from langchain.agents.middleware import wrap_model_call
from openai import RateLimitError
import asyncio
from utils.general_utils.loggers import logger

@wrap_model_call
async def anti_rate_limit(request,handle):
    for i in range(3):
        try:
            response = await handle(request)
            return response
        except RateLimitError as e:
            logger.info("Rate limit error, retrying...")
            await asyncio.sleep(80)

    else:
        raise Exception()