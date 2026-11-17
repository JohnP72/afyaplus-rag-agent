"""Tools available to the AfyaPlus agent."""
import math
import json
from functools import lru_cache

from langchain_core.tools import tool

from src.knowledge import get_index
from src.privacy import PrivacyMasker


@lru_cache(maxsize=1)
def get_retriever():
    """Reuse one retriever instead of loading the index for every query."""
    return get_index().as_retriever(similarity_top_k=3)


@tool
def search_knowledge(query: str) -> str:
    """Search fictional AfyaPlus insurance and clinical routing manuals.

    Use for coverage rules, exclusions, authorisation requirements,
    administrative routing and calculation rules.

    Pass a specific question without personal identifiers.
    Returned passages are candidate evidence, not a confirmed answer.
    Use only passages that directly support the requested information.
    If none support it, report information not found.
    """
    if not query.strip():
        return json.dumps({
            "status": "invalid_input",
            "message": "A search question is required.",
        })

    if len(query) > 1500:
        return json.dumps({
            "status": "invalid_input",
            "message": "Search question must be at most 1500 characters.",
        })

    try:
        # Extra protection before the query reaches the embedding API.
        safe_query = PrivacyMasker().mask(query)
        results = get_retriever().retrieve(safe_query)

        passages = []
        for result in results:
            metadata = result.node.metadata
            passages.append({
                "source": metadata.get("source", "unknown"),
                "section": metadata.get("section", "unknown"),
                "text": result.node.get_content(),
            })

        return json.dumps({
            "status": "candidate_passages" if passages else "not_found",
            "passages": passages,
        }, ensure_ascii=False)

    except Exception:
        # Do not expose raw exceptions, queries or private configuration.
        return json.dumps({
            "status": "error",
            "message": "Knowledge search is unavailable. Refer to staff.",
        })

@tool
def calculate_medication_volume(
    prescribed_dose_mg: float,
    concentration_mg_per_ml: float,
) -> str:
    """Calculate volume from a supplied dose and concentration.

    Args:
        prescribed_dose_mg: Explicitly supplied prescribed dose in mg.
        concentration_mg_per_ml: Explicitly supplied concentration in mg/mL.

    Both inputs must be positive and finite.
    Do not choose a dose or infer a concentration.
    This demonstration calculation requires professional verification
    before any real-world use.
    """
    try:
        values = (prescribed_dose_mg, concentration_mg_per_ml)

        if any(isinstance(value, bool) for value in values):
            raise ValueError("Inputs must be numbers, not true/false.")

        dose = float(prescribed_dose_mg)
        concentration = float(concentration_mg_per_ml)

        if not all(math.isfinite(value) for value in (dose, concentration)):
            raise ValueError("Inputs must be finite numbers.")

        if dose <= 0 or concentration <= 0:
            raise ValueError("Dose and concentration must both exceed zero.")

        volume = dose / concentration

        if not math.isfinite(volume) or volume <= 0:
            raise ValueError("The calculated volume is outside numeric limits.")

        return json.dumps({
            "status": "success",
            "volume_ml": volume,
            "formula": "dose_mg / concentration_mg_per_ml",
            "notice": "Demonstration only; professional verification required.",
        })

    except (TypeError, ValueError, OverflowError, ZeroDivisionError) as error:
        return json.dumps({
            "status": "invalid_input",
            "message": str(error),
        })