# AfyaPlus RAG-Powered Agent System

A Week 2 capstone demonstrating document-grounded insurance information,
administrative clinical routing, validated calculations, session memory,
PII masking and controlled output restoration.

This is an educational prototype using fictional manuals.
It is not a production medical system or a substitute for clinical judgement.

## Architecture

The application processes requests in this order:

1. Receive input through the terminal.
2. Replace supported Kenyan mobile numbers and emails with placeholders.
3. Send masked input and recent masked history to a LangChain tool-calling runner.
4. Retrieve relevant manual passages through LlamaIndex or execute a calculation.
5. Review the draft answer against tool evidence and masked conversation.
6. Restore recognised session placeholders locally before displaying the result.

Original contact details remain in an in-memory session mapping.
Restored answers are not added to model conversation history.

## Project structure

- knowledge-manual/: fictional insurance and routing documents
- src/privacy.py: masking and session-specific restoration
- src/knowledge.py: section parsing, embeddings and local index storage
- src/tools.py: knowledge search and medication-volume calculation
- src/agent.py: bounded tool-calling loop and masked message history
- src/validation.py: model-based evidence review
- src/main.py: interactive terminal application
- tests/test_privacy.py: automated privacy tests
- .env.example: configuration template without secrets
- requirements.txt: direct dependencies
- requirements-lock.txt: recorded installed dependency versions

## Requirements

- Python 3.11
- Git
- An OpenAI API key with access to the configured models
- Internet access for model and embedding requests

The application uses gpt-4.1-mini and text-embedding-3-small.
API usage may incur charges.

## Setup on Windows using Git Bash

```bash
git clone https://github.com/JohnP72/afyaplus-rag-agent.git
cd afyaplus-rag-agent
py -3.11 -m venv .venv311
source .venv311/Scripts/activate
python -m pip install -r requirements-lock.txt
cp .env.example .env
```

Edit .env and replace the placeholder with your own OPENAI_API_KEY.
Never commit the real key.

If Windows Application Control blocks SQLAlchemy's compiled extension,
the following Python-only installation resolved it on the development machine:

```bash
DISABLE_SQLALCHEMY_CEXT=1 python -m pip install --force-reinstall --no-cache-dir --no-binary=SQLAlchemy --no-deps "SQLAlchemy==2.1.9"
```

## Build the knowledge index

```bash
python -m src.knowledge
```

The pipeline reads Markdown manuals, separates topic sections, retains
source metadata and splits longer sections at sentence boundaries.

Embeddings and index data are saved locally under storage/knowledge/.
The saved index is reused on later runs.

After changing a manual, explicitly rebuild:

```bash
python -c "from src.knowledge import get_index; get_index(rebuild=True)"
```

Restart the application after rebuilding so its cached retriever reloads.

## Run the assistant

```bash
python -m src.main
```

Commands:

- /clear: clear conversation history and the private placeholder mapping
- /exit: end the session and clear session data

## Example questions

- What percentage does the patient pay for outpatient consultations?
- What is the annual limit for that benefit?
- What are the requirements for specialist consultations?
- Does the Basic Plan cover dental implants?
- For a supplied dose of 250 mg and concentration of 50 mg/mL,
  calculate the volume.

The fictional outpatient policy specifies a 20% patient contribution
and an annual outpatient benefit limit of KES 50,000.

Dental implant coverage is not specified in the demonstration manuals.
A supplied dose of 250 mg divided by 50 mg/mL gives 5 mL.

## Tools and orchestration

The runner exposes two tools with type hints and descriptive docstrings:

1. search_knowledge retrieves up to three candidate passages with source
   filenames and section names.
2. calculate_medication_volume validates positive, finite inputs and
   calculates volume in mL from dose in mg and concentration in mg/mL.

The agent must not choose doses or infer missing concentrations.
Calculation results require professional verification before real-world use.

LangChain Core and ChatOpenAI provide the tool-calling interface.
The runner explicitly executes requested tools and returns ToolMessages.

## Token and execution management

- User input is limited to 4,000 characters.
- Search questions are limited to 1,500 characters.
- Retrieval returns at most three passages.
- History retains six completed user/assistant exchanges.
- Each turn permits at most five main model calls and six tool executions.
- The main model's output is capped at 700 tokens.
- A separate answer-review request adds latency and token usage.
- The local index and cached retriever reduce repeated document processing.

Character and message limits are practical bounds, not an exact
token-budget calculation.

## Grounding and answer review

Insurance and routing answers should cite:
[source filename | section].

The reviewer compares drafts with current-turn tool evidence.
It also receives masked conversation context for personal-detail references.

If the reviewer rejects a draft or encounters an error, the application
returns a verification fallback rather than releasing the draft.

The review is model-based and can make mistakes.
Retrieval scores are not calibrated guarantees of relevance.

## Privacy safeguards

- Regex middleware masks supported Kenyan mobile formats and emails.
- A session-specific mapping retains originals in memory.
- Model history stores masked messages.
- Search queries receive an additional masking pass.
- De-masking occurs locally at the final display stage.
- Session data is cleared on reset and application exit.
- .env, virtual environments and generated storage are ignored by Git.
- The committed .env.example contains a placeholder only.

Terminal input and final displayed output can contain original details.
Do not use real patient information in demonstrations or screenshots.

## Validation performed during development

- All 23 automated tests passed, covering privacy, calculations,
  tool failures and citation validation.
- All four live retrieval checks passed: each expected source section
  appeared among the top three results.
- The index built 15 chunks from the two demonstration manuals.
- Retrieval returned the outpatient contribution passage.
- The agent answered an insurance question with a citation.
- A follow-up question retained the relevant benefit context.
- An unsupported dental-benefit question returned information not found.
- Valid calculation inputs returned 5 mL.
- Zero concentration returned an error without crashing.
- Email restoration worked across a follow-up exchange.
- A history check confirmed the sample email was absent from masked history.
- Reset cleared conversation history.

Run the automated tests:

```bash
python -m unittest discover -s tests -v
```
Run the live retrieval checks (requires API access):

```bash
python -m tests.check_retrieval
```
## Limitations and compliance considerations

This prototype demonstrates selected privacy safeguards relevant to
data minimisation. It does not establish full compliance with the
Kenya Data Protection Act, 2019.

Regex coverage is limited and does not anonymise every identifier.
Names, addresses, IDs and clinical narratives may still identify a person.
Reversible masking is pseudonymisation rather than irreversible anonymisation.

The prototype does not implement authentication, role-based access,
durable audit logging, automatic index freshness checks or live insurer
eligibility verification.

A real deployment requires appropriate legal, privacy, security and
clinical review, including assessment of external API processing.

## Git workflow

Development takes place on feat-rag-agent-system.
Final delivery requires a pull request into main, actual peer review,
resolution of review feedback and merge.

## Author

Peter John Imaji