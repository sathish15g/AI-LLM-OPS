from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from config.config import Config


class RAGChainBuilder:
    def __init__(self, vector_store):
        self.vector_store = vector_store

        self.model = ChatGroq(
            model=Config.MODEL_NAME,
            temperature=0.5
        )

        self.history_store = {}

    # ✅ Session-based memory
    def _get_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.history_store:
            self.history_store[session_id] = ChatMessageHistory()
        return self.history_store[session_id]

    # ✅ Format docs → string
    def _format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def build_chain(self):

        retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})

        # 🔹 Step 1: Rewrite question (history-aware)
        rewrite_prompt = ChatPromptTemplate.from_messages([
            ("system", "Rewrite the user query into a standalone question."),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ])

        rewrite_chain = (
            rewrite_prompt
            | self.model
            | StrOutputParser()
        )

        # 🔹 Step 2: Retrieval pipeline (IMPORTANT FIX)
        retrieval_chain = (
            RunnableLambda(lambda x: {
                "input": x["input"],
                "chat_history": x.get("chat_history", [])
            })
            | rewrite_chain
            | retriever
        )

        # 🔹 Step 3: QA Prompt
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You're an e-commerce bot answering product-related queries.\n"
             "Use ONLY the context below.\n\nCONTEXT:\n{context}"
            ),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ])

        # 🔹 Step 4: Final RAG chain
        rag_chain = (
            {
                "context": retrieval_chain | RunnableLambda(self._format_docs),

                # Pass input correctly
                "input": RunnableLambda(lambda x: x["input"]),

                # Pass history correctly
                "chat_history": RunnableLambda(lambda x: x.get("chat_history", []))
            }
            | qa_prompt
            | self.model
            | StrOutputParser()
        )

        # 🔹 Step 5: Add memory
        return RunnableWithMessageHistory(
            rag_chain,
            self._get_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )