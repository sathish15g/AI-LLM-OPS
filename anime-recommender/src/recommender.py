from langchain_groq import ChatGroq
from langchain_core.runnables import RunnablePassthrough
from src.prompt_template import get_anime_prompt


class AnimeRecommender:
    def __init__(self, retriever, api_key: str, model_name: str):
        self.llm = ChatGroq(
            api_key=api_key,
            model=model_name,
            temperature=0
        )

        self.retriever = retriever
        self.prompt = get_anime_prompt()

        # Build chain
        self.chain = (
            {
                "context": self.retriever,
                "question": RunnablePassthrough()
            }
            | self.prompt
            | self.llm
        )

    def get_recommendation(self, query: str):
        result = self.chain.invoke(query)
        return result.content  # ChatGroq returns AIMessage