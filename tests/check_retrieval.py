"""Live retrieval checks. Requires the index and an OpenAI API key."""

from src.knowledge import get_index


CASES = [
    (
        "What percentage does the patient pay for outpatient consultations?",
        "insurance_policy.md",
        "Outpatient consultations",
    ),
    (
        "Do specialist consultations require a referral?",
        "insurance_policy.md",
        "Specialist consultations",
    ),
    (
        "Do MRI and CT scans require prior authorisation?",
        "insurance_policy.md",
        "Diagnostic services",
    ),
    (
        "Where should someone with an existing specialist referral book?",
        "clinical_routing.md",
        "Existing specialist referrals",
    ),
]


def main() -> None:
    """Check that each expected section appears in the top three results."""
    retriever = get_index().as_retriever(similarity_top_k=3)
    passed = 0

    for question, source, section in CASES:
        results = retriever.retrieve(question)

        found = any(
            result.node.metadata.get("source") == source
            and result.node.metadata.get("section") == section
            for result in results
        )

        print(f"{'PASS' if found else 'FAIL'}: {question}")
        passed += int(found)

    print(f"\nRetrieval checks passed: {passed}/{len(CASES)}")

    if passed != len(CASES):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

    