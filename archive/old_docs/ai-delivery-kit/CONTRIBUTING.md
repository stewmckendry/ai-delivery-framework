# ✍️ CONTRIBUTING to the AI Delivery Kit

Thank you for improving the way we build AI systems! This repo uses a structured patch workflow:

1. Use `generate_patch.py` to submit work
2. Append to:
   - `logs/changelog.yaml`
   - `logs/thought_trace.yaml`
   - `logs/handoff_log.yaml` (if handing off)
3. Optionally generate a `docs/handoff/*.md` note
4. Trigger summary with `--summary`
5. All `.diff` files go in `.patches/`

See `docs/POD_CONTRIBUTING_Guide.md` for pod responsibilities.
