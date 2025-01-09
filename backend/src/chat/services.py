from src.pipelines.user_query import UserQueryPipeline
from src.config import get_settings

settings = get_settings()

user_query_pipeline = UserQueryPipeline(index=settings.INDEX_NAME)


def get_chat_response(message: str, custom_dataset: bool) -> str:
    resp = user_query_pipeline.ask(message)
    return resp
