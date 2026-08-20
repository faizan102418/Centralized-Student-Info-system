# Research Evaluation Methodology

This document defines how we measure the system honestly, from the first
day of Phase 1 onward. The core rule: **decide what "good" means and how
we'll measure it before we know the answer.** Everything here should be
written before the corresponding feature is built, not after, so we never
end up choosing a metric because it happened to look good in hindsight.

This builds directly on the thesis's own Chapter 9 (Testing and
Evaluation) — we're extending that methodology, not replacing it.

---

## 1. Research framing (working, not final)

Two honest framings, ranked by how defensible they are in an interview:

1. **"A comparative study of retrieval strategies for small, multi-table
   institutional databases: keyword search vs. dense vector RAG vs.
   LLM-orchestrated tool-calling."** — Neutral, testable, doesn't presume
   the answer. This is the safer framing.
2. **"Privacy-aware conversational access to student records: measuring
   the accuracy/access-control trade-off in a role-scoped RAG system."**
   — More novel, ties into the RBAC work, but needs the access-control
   evaluation (Section 6) to actually be rigorous to earn this framing.

Avoid: any title that asserts a result ("A superior/novel/highly accurate
system for...") before the data exists. Titles should describe *what was
studied*, not *what you hope was found*.

## 2. Baselines — what we compare against

A number on its own means nothing. Every metric below is measured against
these three baselines, run on the *same* query set:

| Baseline | What it is |
|---|---|
| B0 — Regex MVP | The original thesis system (name-extraction regex + Groq) |
| B1 — Keyword/SQL search | Direct `LIKE` queries against MySQL, no vector store |
| B2 — Raw LLM, no RAG | Groq API given the question with no retrieved context at all |
| **System** | The current tool-calling / hybrid-search version |

If the new System doesn't clearly beat B1 and B2 on some query types, that
is a real, reportable finding — not a failure to hide. "RAG helps for
lookup queries but not for general questions" is a legitimate, publishable
result.

## 3. Query logging schema (implement in Week 1)

Every query — including our own dev/testing traffic — gets logged from
day one. Add this table alongside the `users` table:

```sql
CREATE TABLE IF NOT EXISTS query_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_id VARCHAR(64) NOT NULL,          -- random per-session token, not tied to real identity
    user_role ENUM('admin','faculty','student','dev_test') NOT NULL,
    query_text TEXT NOT NULL,
    detected_intent VARCHAR(50),              -- e.g. 'lookup', 'compare', 'general'
    extracted_entities JSON,                  -- e.g. {"student_names": ["Alice Smith"]}
    system_variant VARCHAR(20) NOT NULL,      -- 'B0_regex' | 'B1_keyword' | 'B2_raw_llm' | 'system'
    retrieved_chunk_ids JSON,
    response_text TEXT,
    latency_ms INT,
    access_denied BOOLEAN DEFAULT FALSE,      -- did RBAC block this query?
    user_feedback ENUM('up','down','none') DEFAULT 'none',
    human_label ENUM('correct','partial','incorrect','not_rated') DEFAULT 'not_rated',
    notes TEXT
);
```

**Privacy rule, non-negotiable:** `session_id` is a random token, never a
real name/email. `query_text` and `response_text` will contain real
student names during the pilot — this table is **never** exported or
made public as-is. Anything shared in a paper/GitHub gets pulled from
`data/eval/anonymized_queries.json` (Section 7), not this table directly.

## 4. Building the evaluation query set

Two tiers, kept strictly separate:

**Tier A — Seed set (start here, Week 1).** Expand the thesis's own
Chapter 9.2 test cases (name extraction phrasings, query-type cases,
error-handling cases) into a fixed, version-controlled file:
`data/eval/seed_queries.jsonl`, one query per line with an expected
answer or expected behavior (e.g. "should refuse — out of scope").
Roughly 60-100 queries, stratified across: single-student lookup,
comparison queries, general/off-topic questions, ambiguous phrasing,
non-existent students, and access-control edge cases (student asking
about another student).

**Tier B — Real pilot queries (Week 7+, after informed consent).**
Once real users are querying the deployed system, sample from
`query_logs` for held-out evaluation. **Never** tune prompts or retrieval
logic against Tier B data you're also using to report results — that's
the same mistake as testing on your training set. Split: 70% for
iterating on the system, 30% locked aside untouched until final
evaluation.

## 5. Metrics

| Level | Metric | How measured |
|---|---|---|
| Retrieval | Precision/recall of retrieved chunks | Hand-label ~30 queries with "gold" chunks once; compare |
| Answer | Correctness (3-point: correct / partial / incorrect) | Human-rated, rubric below |
| Answer | Groundedness | Is every claim in the answer traceable to a retrieved chunk? Human-checked |
| Access control | Leak rate | % of out-of-scope queries where a student role received another student's data (target: 0%, and this must be reported even if not 0%) |
| System | Latency (p50/p95) | From `latency_ms`, per system_variant |
| Real usage | Thumbs up/down rate over time | From `user_feedback`, weekly rolling |

## 6. Human evaluation protocol

Write the rubric **before** rating anything:

- **Correct** — factually matches the database, fully answers the question
- **Partial** — right student/data, but incomplete or slightly imprecise
- **Incorrect** — wrong data, hallucinated info, or wrong student

Rate blind where possible: strip the `system_variant` label before
handing queries to a rater so the score isn't influenced by knowing which
system produced it. If a second rater is available (classmate, supervisor,
Mr. Imran ud Din), have them independently rate a 20-30 query subset and
report agreement (Cohen's kappa) — even a small inter-rater check adds
real credibility and costs one afternoon.

## 7. Statistical honesty checklist

- Always report **n** (sample size) next to any percentage. "94% (47/50)"
  is honest; "94% accuracy" alone is not.
- Don't cherry-pick the query set after seeing results. Freeze
  `seed_queries.jsonl` before running any evaluation pass.
- Report the failure cases explicitly in whatever you write up — a
  results section with zero weaknesses reads as unreliable, not
  impressive.
- Before creating any public dataset (`anonymized_queries.json` for
  GitHub/arXiv), strip real names/roll numbers and replace with the
  synthetic ones from `data/seed.sql` (Alice Smith, Bob Johnson, etc.)
  or clearly synthetic placeholders — never publish real student data.

## 8. Consent and pilot ethics

Before any real user's queries are logged for evaluation purposes (not
just app functionality):
- Tell them plainly: queries are logged for system improvement and
  possible research use, session-anonymized, never published with real
  identities.
- Get explicit opt-in (a checkbox at login is enough at this scale).
- Anyone can request their session's logs be deleted.

## 9. Timeline

| Weeks | Activity |
|---|---|
| 1 | Implement `query_logs`, freeze `seed_queries.jsonl` (Tier A) |
| 1-6 | Every dev/test query logged with `system_variant` tagged correctly as features land |
| 7-9 | Pilot with real users, consent flow live, Tier B collection begins |
| 10 | Run all 4 system variants against Tier A + held-out Tier B, human-rate |
| 11 | Compute metrics, inter-rater check, write results honestly (including weaknesses) |
| 12 | Draft write-up, anonymize any dataset intended for public release |
