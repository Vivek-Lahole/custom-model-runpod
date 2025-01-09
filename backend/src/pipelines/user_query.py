from src.retriever.qdrant_retriever import QdrantRetriever
from src.embedder.text_embedder import TextEmbedder
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.components.builders import ChatPromptBuilder
from haystack.dataclasses import ChatMessage
from src.pipelines.document_indexing import DocumentIndexingPipeline
from src.stores.qdrant import DocumentStoreInstance
from haystack.components.generators.utils import print_streaming_chunk
from haystack import Pipeline
from dotenv import load_dotenv
import os
from haystack.utils import Secret
from src.config import get_settings
from datasets import load_dataset
from haystack.dataclasses import Document


settings = get_settings()
load_dotenv()


class UserQueryPipeline:
    def __init__(self, index: str):
        self._load_variables()
        self._init_components(index)
        self._setup_pipeline()

    def _load_variables(self):
        self.api_key = settings.RUNPOD_API_KEY
        if not self.api_key:
            raise EnvironmentError("RUNPOD_API_KEY environment variable is not set!")
        self.api_key_secret = Secret.from_token(self.api_key)

        self.runpod_id = settings.RUNPOD_ENDPOINT_ID
        if not self.runpod_id:
            raise EnvironmentError(
                "RUNPOD_ENDPOINT_ID environment variable is not set!"
            )

    def _get_template(self):
        return [
            ChatMessage.from_system(
                """
            You are Snoop Dogg, the famous rapper and cultural icon. Keep responses brief and concise, under 
            50 words. Use your unique style to answer sarcastically with gansgter vibe and slang.
            """
            ),
            ChatMessage.from_user(
                """
            Context:
            {% for document in documents %}
                {{ document.content | truncate(500) }}
            {% endfor %}

            Question: {{ question }}
            Answer:
            """
            ),
        ]

    def _init_components(self, index: str):
        self.document_store = DocumentStoreInstance.get_instance(
            url=settings.QDRANT_URL,
            index=index,
            embedding_dim=settings.EMBEDDING_DIM,
            recreate_index=False,
        )

        if self.document_store.count_documents() == 0:
            indexing_pipeline = DocumentIndexingPipeline()
            dataset = load_dataset(
                "huggingartists/snoop-dogg", cache_dir="./src/data/snoop_dogg_cache"
            )
            documents = [Document(content=item["text"]) for item in dataset["train"]]
            indexing_pipeline.run(documents)

        self.text_embedder = TextEmbedder.get_instance(
            model=settings.EMBEDDING_MODEL,
        )

        self.retriever = QdrantRetriever.get_instance()

        self.prompt_builder = ChatPromptBuilder(
            template=self._get_template(),
        )

        self.chat_generator = OpenAIChatGenerator(
            model=settings.LLM_MODEL,
            api_base_url=f"https://api.runpod.ai/v2/{self.runpod_id}/openai/v1",
            api_key=self.api_key_secret,
            streaming_callback=print_streaming_chunk,
            timeout=50,
            max_retries=3,
            generation_kwargs={
                "temperature": 0.7,
                "max_tokens": 300,
            },
        )

    def _setup_pipeline(self):
        self.pipeline = Pipeline()
        self.pipeline.add_component("text_embedder", self.text_embedder)
        self.pipeline.add_component("retriever", self.retriever)
        self.pipeline.add_component("prompt_builder", self.prompt_builder)
        self.pipeline.add_component("llm", self.chat_generator)

        self.pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
        self.pipeline.connect("retriever.documents", "prompt_builder.documents")
        self.pipeline.connect("prompt_builder.prompt", "llm.messages")

    def ask(self, question: str) -> str:
        try:
            response = self.pipeline.run(
                {
                    "text_embedder": {"text": question},
                    "prompt_builder": {"question": question},
                }
            )

            if (
                not response
                or not response.get("llm")
                or not response["llm"].get("replies")
            ):
                return "Yo, my bad! I'm having trouble processing that right now , gotta get my mind right. Mind trying again?"
            return response["llm"]["replies"][0].text
        except IndexError:
            return "Fo' shizzle, something went wrong with the response. Can you rephrase your question?"
        except Exception as e:
            print(f"Error running pipeline: {str(e)}")
            return "My bad, homie! Something ain't right with this weed nigga ! Give it another shot!"
