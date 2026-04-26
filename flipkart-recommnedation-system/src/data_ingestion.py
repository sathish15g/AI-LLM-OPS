from langchain_astradb import AstraDBVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from src.data_converter import DataConverter
from config.config import Config

import os

class DataIngestion:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL_NAME)
        self.vstore = AstraDBVectorStore(
            embedding= self.embeddings,
            api_endpoint=Config.ASTRA_DB_API_ENDPOINT,
            token=Config.ASTRA_DB_APPLICATION_TOKEN,
            collection_name="flipkart_database"
        )

    def ingest_data(self,load_exiting=True):
        if load_exiting:
            print("Loading existing data from AstraDB...")
            return self.vstore
     
        print("Ingesting new data into AstraDB...")


        file_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "data",
            "flipkart_product_review.csv"
        )

        data_converter = DataConverter(file_path)
        documents = data_converter.convert_to_documents()
        self.vstore.add_documents(documents=documents)
        print("Data ingestion completed successfully.")
        
if __name__ == "__main__":
    data_ingestion = DataIngestion()
    data_ingestion.ingest_data(load_exiting=False)

    
