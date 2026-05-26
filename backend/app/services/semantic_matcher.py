from typing import Any
import re
from sentence_transformers import SentenceTransformer, util


def _tokenize(text: str) -> set[str]:
    words = re.findall(r"[A-Za-zÀ-ÿ0-9+#.-]+", text.lower())
    return {word for word in words if len(word) > 2}


def match_semantic(cv_text: str, job_text: str) -> dict[str, Any]:
    job_tokens = _tokenize(job_text)
    cv_tokens = _tokenize(cv_text)

    if not job_tokens:
        return {
            "score": 0.0,
            "details": {"matched_terms": [], "missing_terms": [], "coverage": 0.0},
        }

    matched = sorted(job_tokens.intersection(cv_tokens))
    missing = sorted(job_tokens.difference(cv_tokens))
    coverage = len(matched) / len(job_tokens)

    print(f"[Semantic Matcher] Job tokens: {len(job_tokens)}, CV tokens: {len(cv_tokens)}")
    print(f"[Semantic Matcher] Matched tokens: {len(matched)}, Missing tokens: {len(missing)}, Coverage: {coverage:.2%}")

    return {
        "score": round(coverage * 100, 2),
        "details": {
            "matched_terms": matched,
            "missing_terms": missing,
            "coverage": round(coverage * 100, 2),
        },
    }


# Load once — ~90MB model, cached after first download
# pip install sentence-transformers
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
# ↑ handles French + English; swap for "all-MiniLM-L6-v2" if English-only

TECH_SKILLS = {
    "java", "python", "javascript", "typescript", "c++", "go", "rust",
    "spring", "django", "react", "fastapi", "nodejs", "spring boot",
    "postgresql", "mysql", "mongodb", "redis",
    "docker", "kubernetes", "aws", "azure", "gcp", "terraform",
}

def skill_overlap_multiplier(cv_text: str, job_text: str) -> float:
    """Returns a multiplier between 0.4 and 1.0 based on hard skill overlap.
    0% skill match → score × 0.4, 100% skill match → score × 1.0.
    """
    cv_lower  = cv_text.lower()
    job_lower = job_text.lower()

    job_skills = {s for s in TECH_SKILLS if s in job_lower}
    if not job_skills:
        return 1.0  # no detectable tech skills in job offer → no penalty

    cv_skills     = {s for s in job_skills if s in cv_lower}
    overlap_ratio = len(cv_skills) / len(job_skills)

    print(f"Job skills found: {job_skills}")

    print(f"[Skill Multiplier] Job skills: {job_skills}, CV matched: {cv_skills}, Overlap: {overlap_ratio:.2%}")

    return 0.3 + (0.7 * overlap_ratio)


def extract_dense_content(text: str) -> str:
    """Keep only high-signal lines: skills, requirements, experience, tools."""
    high_signal_patterns = [
        r"(?i)(compétences?|skills?|technologies?|outils?|tools?)",
        r"(?i)(expérience?|experience|requis|required|qualif)",
        r"(?i)(java|python|sql|aws|docker|spring|kubernetes)",  # expand as needed
    ]
    lines = text.split("\n")
    scored_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        weight = sum(1 for p in high_signal_patterns if re.search(p, line))
        if weight > 0:
            scored_lines.append(line)

    # Fall back to full text if nothing matched
    return "\n".join(scored_lines) if scored_lines else text


def match_semantic_transformer(cv_text: str, job_text: str) -> dict[str, Any]:
    # ── 0. Extract dense content for higher-signal comparison ──
    cv_dense  = extract_dense_content(cv_text)
    job_dense = extract_dense_content(job_text)

    # ── 1. Full-document embedding similarity (on dense content) ──
    embeddings     = model.encode([cv_dense, job_dense], convert_to_tensor=True)
    semantic_score = float(util.cos_sim(embeddings[0], embeddings[1]))

    # ── 2. Apply skill multiplier to penalize missing hard skills ──
    multiplier  = skill_overlap_multiplier(cv_text, job_text)
    final_score = semantic_score * multiplier

    # ── 3. Section-level matching (more granular signal) ──
    job_sentences = [s.strip() for s in re.split(r"[.\n]", job_dense) if len(s.strip()) > 20]
    cv_embedding  = model.encode(cv_dense, convert_to_tensor=True)

    section_scores = []
    for sentence in job_sentences:
        sent_emb = model.encode(sentence, convert_to_tensor=True)
        score    = float(util.cos_sim(cv_embedding, sent_emb))
        section_scores.append({"requirement": sentence, "match_score": round(score * 100, 2)})

    section_scores.sort(key=lambda x: x["match_score"])

    # ── 4. Derive strengths/weaknesses from section scores ──
    threshold  = 60.0
    strengths  = [s["requirement"] for s in section_scores if s["match_score"] >= threshold]
    weaknesses = [s["requirement"] for s in section_scores if s["match_score"] <  threshold]

    print(f"[Transformer Matcher] Semantic: {semantic_score:.2%}, Multiplier: {multiplier:.2f}, Final: {final_score:.2%}")

    return {
        "score": round(final_score * 100, 2),
        "details": {
            "semantic_similarity":  round(semantic_score * 100, 2),
            "skill_multiplier":     round(multiplier, 2),
            "section_breakdown":    section_scores,
            "matched_requirements": strengths,
            "missing_requirements": weaknesses,
        },
    }