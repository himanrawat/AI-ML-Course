# ======================================
# TOPIC: ROLE PROMPTING AND CONTEXTUAL PROMPTING
# LEVEL: BEGINNER
# ID: prompt-engineering.foundations.role-context
# ======================================

# INTRODUCTION
# "You are an expert..." is the most copied prompt trick - and the most
# misunderstood. Roles help mostly by bringing CONTEXT: audience, standards and
# priorities. Contextual prompting is about giving the model what it cannot know.
#
# THEORY
# ROLE PROMPTING:
# - Assigning a role ("You are a senior security reviewer") shifts tone,
#   vocabulary, level of detail and which concerns get attention.
# - A role does NOT add knowledge or make the model more accurate by itself.
#   "World-class expert" adds little; a SPECIFIC role with responsibilities and
#   standards adds a lot ("You review pull requests for a payments company;
#   you prioritise security and correctness over style").
# - Roles work best in the system prompt and combined with explicit criteria.
# CONTEXTUAL PROMPTING:
# - Supply facts the model lacks: company policies, product details, user
#   profile, the current date, previous decisions, the document to work on.
# - Explain the situation and goal: who will read the output, what decision it
#   supports, what "good" looks like.
# - Relevant context beats more context: irrelevant text distracts and costs
#   tokens.
# - This is the bridge to CONTEXT ENGINEERING and RAG (retrieving the right
#   context automatically).
#
# REAL-WORLD ANALOGY
# Telling a consultant "act like a lawyer" changes their vocabulary; handing
# them the actual contract, the client's goal and the deadline changes the
# quality of their advice.
#
# SYNTAX:
#   system = "You are <specific role> at <organisation>. You care about <criteria>."
#   user = "<context>...</context> <task>...</task>"
#
# SMALL WORKING EXAMPLE:
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from course_llm import complete

code = '''def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query)'''

generic = f"You are a world-class expert programmer. Review this code:\n{code}"
specific_system = ("You review Python pull requests for a fintech company. "
                   "Priorities, in order: security, correctness, maintainability. "
                   "Report only issues that matter for production; skip style nits.")
context = {
    "today": date(2026, 11, 1).isoformat(),
    "service": "public REST API, user_id comes from the URL path",
    "database": "PostgreSQL via psycopg",
    "reader": "a junior developer who will fix the issues",
}
context_block = "\n".join(f"- {k}: {v}" for k, v in context.items())
specific_user = (f"<context>\n{context_block}\n</context>\n\n<code>\n{code}\n</code>\n\n"
                 "List each issue as: severity (high/medium/low), problem, fix (with corrected code).")
print(generic, "\n" + "=" * 40)
print(specific_system, "\n", specific_user, sep="")
print("=" * 40)
print(complete(specific_user, system=specific_system, offline=(
    "high - SQL injection: user_id from the URL is formatted into SQL.\n"
    "fix: db.execute(\"SELECT * FROM users WHERE id = %s\", (user_id,))\n"
    "medium - SELECT * returns sensitive columns; select only needed fields.")))

# EXPLANATION (LINE BY LINE):
# generic                  -> a vague "expert" role and no context: the review
#                             may focus on style or miss the threat model.
# specific_system          -> a concrete role with priorities and scope.
# context                  -> facts the model cannot know: where user_id comes
#                             from makes SQL injection clearly high severity.
# "reader" in context      -> shapes the explanation level.
# Output format line       -> makes results consistent and actionable.
#
# COMMON MISTAKES:
# 1. Believing "You are an expert" improves factual accuracy.
# 2. Giving a role but no task criteria.
# 3. Pasting huge irrelevant context "just in case".
# 4. Forgetting dynamic facts like today's date or the user's plan.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write three versions of a prompt explaining recursion: no role, a generic
# role, and a specific role + context (audience: JS developer learning Python,
# purpose: interview prep). Predict the differences in comments.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write build_context(user, request) that assembles only RELEVANT context for
# a customer-support prompt from a user profile dict with 15 fields (plan,
# country, last orders, preferences...). Decide relevance by request type and
# explain your choices.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Run an experiment (API access needed, or design it fully): same task, 4
# variants - no role, generic expert role, specific role, specific role +
# context. Define a rubric before running, evaluate 5 inputs per variant,
# and write a conclusion about what actually improved quality.

# YOUR CODE:

