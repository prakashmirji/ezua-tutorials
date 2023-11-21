from typing import List

import torch
from langchain_core.schema.embeddings import Embeddings


class MLDEEmbeddings(Embeddings):
    def __init__(self, tokenizer, model):
        self.tokenizer = tokenizer
        self.model = model

    def _tokenize(self, texts: List[str]) -> List[List[int]]:
        return self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            return_tensors="pt",
        ).to(self.model.device)
    
    def _encode(self, tokens: List[List[int]]) -> List[List[float]]:
        with torch.no_grad():
            # Get hidden state of shape [bs, seq_len, hid_dim]
            last_hidden_state = self.model(
                tokens["input_ids"], output_hidden_states=True, return_dict=True
            ).hidden_states[-1]

        # Get weights of shape [bs, seq_len, hid_dim]
        weights = (
            torch.arange(start=1, end=last_hidden_state.shape[1] + 1)
            .unsqueeze(0)
            .unsqueeze(-1)
            .expand(last_hidden_state.size())
            .float()
            .to(last_hidden_state.device)
        )

        # Get attn mask of shape [bs, seq_len, hid_dim]
        input_mask_expanded = (
            tokens["attention_mask"]
            .unsqueeze(-1)
            .expand(last_hidden_state.size())
            .float()
        )

        # Perform weighted mean pooling across seq_len: bs, seq_len, hidden_dim -> bs, hidden_dim
        sum_embeddings = torch.sum(
            last_hidden_state * input_mask_expanded * weights, dim=1)
        sum_mask = torch.sum(input_mask_expanded * weights, dim=1)

        embeddings = sum_embeddings / sum_mask     
        return embeddings[0].tolist()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        features = []
        for text in texts:
            tokens = self._tokenize([text])
            embeddings = self._encode(tokens)
            features.append(embeddings)
        return features

    def embed_query(self, text: str) -> List[float]:
        tokens = self._tokenize([text])
        return self._encode(tokens)
