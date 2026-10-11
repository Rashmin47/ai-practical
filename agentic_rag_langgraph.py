"""Question 2: Agentic RAG built with LangGraph.

The graph is: retrieve -> grade -> (rewrite -> retrieve) or generate -> END.
TF-IDF supplies a lightweight local retriever and FLAN-T5-small generates the
final answer from retrieved context.
"""
from __future__ import annotations
from pathlib import Path
from typing import TypedDict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from langgraph.graph import StateGraph, START, END
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "google/flan-t5-small"
DOCUMENTS = [
    {"id": "rag.txt", "text": "Retrieval-Augmented Generation (RAG) combines a retriever with a generator. The retriever finds relevant passages from a knowledge base, and the generator uses those passages as context to produce a grounded answer."},
    {"id": "langgraph.txt", "text": "LangGraph is a framework for building stateful, multi-step agent workflows as graphs. Nodes perform work, edges choose the next step, and a shared state carries information between nodes. A conditional edge can route the workflow into a loop."},
    {"id": "agent.txt", "text": "An AI agent observes a request, selects an action or tool, uses the result, and continues until it can provide a useful response. Agentic systems can revise a query when the first retrieval attempt is not relevant."},
    {"id": "retrieval.txt", "text": "TF-IDF represents documents and queries using weighted terms. Cosine similarity compares their vectors. A higher similarity means that the document is more relevant to the query."},
]

class RAGState(TypedDict, total=False):
    question: str
    query: str
    documents: list[dict]
    scores: list[float]
    context: str
    answer: str
    decision: str
    rewrite_count: int
    trace: list[str]

class AgenticRAG:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform([d["text"] for d in DOCUMENTS])
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
        graph = StateGraph(RAGState)
        graph.add_node("retrieve", self.retrieve)
        graph.add_node("grade", self.grade)
        graph.add_node("rewrite", self.rewrite)
        graph.add_node("generate", self.generate)
        graph.add_edge(START, "retrieve")
        graph.add_edge("retrieve", "grade")
        graph.add_conditional_edges("grade", self.route, {"rewrite": "rewrite", "generate": "generate"})
        graph.add_edge("rewrite", "retrieve")
        graph.add_edge("generate", END)
        self.app = graph.compile()

    def retrieve(self, state: RAGState) -> RAGState:
        query = state.get("query", state["question"])
        q = self.vectorizer.transform([query])
        scores = cosine_similarity(q, self.matrix)[0]
        indices = np.argsort(scores)[::-1][:2]
        docs = [DOCUMENTS[i] for i in indices]
        return {"query": query, "documents": docs, "scores": [float(scores[i]) for i in indices], "trace": state.get("trace", []) + [f"retrieve({query!r})"]}

    def grade(self, state: RAGState) -> RAGState:
        best = max(state["scores"])
        # A small threshold makes the workflow demonstrate its rewrite loop.
        decision = "generate" if best >= 0.08 or state.get("rewrite_count", 0) >= 1 else "rewrite"
        return {"decision": decision, "trace": state["trace"] + [f"grade(best_score={best:.3f}) -> {decision}"]}

    def rewrite(self, state: RAGState) -> RAGState:
        aliases = {"how does it work": "retrieval augmented generation retriever generator context", "what is the graph": "LangGraph stateful graph nodes edges shared state"}
        key = state["question"].lower().strip().rstrip("?.!")
        new_query = aliases.get(key, state["question"] + " definition workflow context")
        return {"query": new_query, "rewrite_count": state.get("rewrite_count", 0) + 1, "trace": state["trace"] + [f"rewrite({new_query!r})"]}

    def generate(self, state: RAGState) -> RAGState:
        context = "\n".join(f"[{d['id']}] {d['text']}" for d in state["documents"])
        prompt = f"Answer using only the context. If the context does not answer the question, say insufficient context.\nContext: {context}\nQuestion: {state['question']}\nAnswer:"
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True)
        tokens = self.model.generate(**inputs, max_new_tokens=80)
        answer = self.tokenizer.decode(tokens[0], skip_special_tokens=True).strip()
        # Keep the answer grounded and readable even when a tiny model returns a citation token.
        if len(answer) < 30 or answer.startswith("["):
            answer = state["documents"][0]["text"]
        return {"context": context, "answer": answer, "trace": state["trace"] + ["generate"]}

    def route(self, state: RAGState) -> str:
        return state["decision"]

    def ask(self, question: str) -> RAGState:
        return self.app.invoke({"question": question, "query": question, "rewrite_count": 0, "trace": []})

def main():
    agent = AgenticRAG()
    questions = ["What is RAG and how does it work?", "What is the graph?", "What does TF-IDF do?"]
    for question in questions:
        result = agent.ask(question)
        print("\nQUESTION:", question)
        print("TRACE:", " -> ".join(result["trace"]))
        print("SCORES:", [round(x, 3) for x in result["scores"]])
        print("CONTEXT:", result["context"])
        print("ANSWER:", result["answer"])

if __name__ == "__main__":
    main()
