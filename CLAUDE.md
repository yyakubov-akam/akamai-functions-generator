# Akamai Functions Code Generation Rules

## Learn Before Coding

Before writing any code, read @docs/_compiled/functions-reference.md

## Think Before Coding

Don't assume. Don't hide confusion. Surface tradeoffs.

Before implementing:

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## Output Structure

All generated functions must be written to /functions/<function_name>/ where <function_name> is a short, descriptive, lowercase-hyphenated name derived from the task (e.g. echo-request-headers, geo-based-redirect).
