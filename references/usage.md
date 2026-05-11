# Usage Overview

This skill is designed to be low-friction after clone.

## Expectations
- No build step is required.
- Python 3.8+ is the script runtime.
- If `xmllint` or `lxml` is already available, validation can run immediately.
- Additional Python packages listed in `scripts/requirements.txt` are optional accelerators, not mandatory installation prerequisites.

## Typical flow
1. Edit an RQML document.
2. Run validation.
3. Run semantic lint or trace analysis when needed.
4. Use extraction and matrix scripts for downstream review artifacts.
