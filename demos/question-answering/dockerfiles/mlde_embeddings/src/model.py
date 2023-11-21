import logging
import argparse

import torch
from kserve import Model, ModelServer
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from transformers import AutoTokenizer, AutoModelForCausalLM

from encoder import MLDEEmbeddings

logger = logging.getLogger(__name__)

DEFAULT_NUM_DOCS = 2


# data = {
#   "instances": [{
#       "input": "How do I configure users?",
#       "num_docs": 4
#   }]
# }

# data = {
#   "instances": [{
#       "query": "add",
#       "docs": [{
#           "content": "...",
#           "title": "...",
#           "source": "..."
#       }]
#   }]
# }


class VectorStore(Model):
    def __init__(self, name: str, persist_dir: str, model_path: str):
        super().__init__(name)
        self.name = name
        self._prepare_vectorstore(persist_dir, model_path)
        self.splitter = CharacterTextSplitter(
            chunk_size=500, chunk_overlap=50)

        self.ready = True

    def _load_model(self, model_path):
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            trust_remote_code=True,
            torch_dtype=torch.bfloat16,
            low_cpu_mem_usage=True,
        ).to("cuda")
        return MLDEEmbeddings(tokenizer, model)

    def _prepare_vectorstore(self, persist_dir: str, model_path: str):
        embeddings = self._load_model(model_path)
        self.vectordb = Chroma(persist_directory=persist_dir,
                               embedding_function=embeddings)

    def predict(self, request: dict, headers: dict) -> dict:
        data = request["instances"][0]

        query = data["input"]
        num_docs = data.get("num_docs", DEFAULT_NUM_DOCS)

        logger.info(f"Received question: {query}")

        docs = self.vectordb.similarity_search(query, k=num_docs)

        logger.info(f"Retrieved context: {docs}")

        return {"predictions": [doc.page_content for doc in docs]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="VectorStore",
                                     description="VectorStore server")
    parser.add_argument("--persist-dir", type=str, required=True,
                        help="The name of the collection.")
    parser.add_argument("--model-path", type=str, required=True,
                        help="The location of the model.")
    args = parser.parse_args()

    model = VectorStore("vectorstore", args.persist_dir, args.model_path)
    ModelServer(workers=1).start([model])
