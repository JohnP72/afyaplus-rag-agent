"""Run the AfyaPlus demonstration assistant in the terminal."""

from src.agent import AfyaAgent


def main() -> None:
    """Handle a single local conversation and restore final output."""
    agent = AfyaAgent()

    print("AfyaPlus demonstration assistant")
    print("Uses fictional manuals; not for real clinical decisions.")
    print("Type /clear to reset the conversation or /exit to quit.")

    try:
        while True:
            question = input("\nYou: ").strip()

            if question.lower() == "/exit":
                break

            if question.lower() == "/clear":
                agent.clear()
                print("Conversation and private mapping cleared.")
                continue

            if not question:
                continue

            masked_answer = agent.ask(question)

            # Restore only this session's recognised placeholders.
            # Never put the restored answer into model history.
            display_answer = agent.masker.restore(masked_answer)

            print(f"\nAfyaPlus: {display_answer}")

    except (KeyboardInterrupt, EOFError):
        print("\nSession ended.")

    finally:
        agent.clear()


if __name__ == "__main__":
    main()

    