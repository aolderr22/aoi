from app.rag.retrieve import Retriever

retriever = Retriever()

results = retriever.retrieve(
    "I need to update HCO_ID references"
)

for result in results:
    print("=" * 50)
    print(result["metadata"])
    print(result["document"])
    print("Distance:", result["distance"])