from qa import generate_answer

while True:

    question = input("\nAsk a question (or type exit): ")

    if question.lower() == "exit":
        break

    result = generate_answer(question)

    print("\nAnswer:")
    print(result["answer"])

    print("\nTimestamp:")
    print(result["timestamp"])

    print("\nRelevant Transcript:")
    print(result["segments"][0]["text"])