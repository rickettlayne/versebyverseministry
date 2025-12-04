import chromadb
from openai import OpenAI

from ingest.config import CHROMA_PATH, COLLECTION_NAME, TOP_K

client = OpenAI(api_key="YOUR_OPENAI_KEY")  # env variable in real code
chroma = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma.get_or_create_collection(COLLECTION_NAME)

def retrieve_context(query: str):
    results = collection.query(
        query_texts=[query],
        n_results=TOP_K
    )
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    return list(zip(docs, metas))

def build_prompt(user_question: str, context_pairs):
    context_strs = []
    for doc, meta in context_pairs:
        src = meta.get("source", "unknown")
        context_strs.append(f"Source: {src}\n{doc}")
    context_block = "\n\n".join(context_strs)

    system_msg = (
        "You are a helpful assistant that answers questions using the provided context. "
        "If the answer is not clearly in the context, say you do not know."
    )

    prompt = f"""
Context:
{context_block}

Question:
{user_question}

Answer using only the context above.
"""
    return system_msg, prompt

def answer_question(question: str) -> str:
    context_pairs = retrieve_context(question)
    system_msg, prompt = build_prompt(question, context_pairs)

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt},
        ]
    )
    return resp.choices[0].message.content.strip()
