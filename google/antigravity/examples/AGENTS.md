<!-- mdformat global-off -->
# SDK Examples

Guidelines for authoring and maintaining examples in this directory.

## Quality Gates

-   **Run every example E2E before committing.** Interactive examples
    must launch, accept at least one prompt, produce a semantically
    correct response, and exit cleanly. Scripted examples must print
    their own PASS/FAIL summary.
-   **Verify semantic output.** Don't just check "no crash" — read the
    response and confirm it answers the prompt. A blank or nonsensical
    response is a failing test.
-   **Verify model names exist.** Never invent model names. Default to
    `gemini-3-flash-preview` unless the feature requires a specific
    model. Confirm the name resolves before uploading.

## 3P Awareness

This is a 3P SDK. External users don't have `blaze`.

-   **Docstring run instructions use `python`, not `blaze`.**
    ```
    To run:
      python thinking_example.py
    ```
-   Use `bazel build` / `bazel run` internally for verification, but
    keep bazel out of the example's public docstring.

## Style

-   **Apache 2.0 header** on every file.
-   **Module-level docstring** explaining what the example demonstrates,
    listing the `python` run command and any useful flag overrides.
-   **One feature per example.** Each example isolates a single SDK
    feature. Don't kitchen-sink multiple concepts into one file.
-   **No private API access.** Don't reach into `agent._conversation`
    or similar underscored attributes. If the public API can't do it,
    that's a gap to file, not a pattern to copy.
-   **No output truncation.** Never slice `step.content`,
    `step.thinking`, etc. (e.g. `[:200]`). Display full model output.
-   **Two-space indent on terminal output.** All printed output uses a
    two-space prefix for visual nesting. Emoji/label prefixes sit after
    the indent:
    ```python
    print(f"\n  💭 Thinking: {step.thinking}")
    print(f"  >>> {prompt}")
    ```
-   **Flags.** Use module-level `_UPPER_CASE` names with
    `flags.DEFINE_string` / `DEFINE_enum_class`. Default model to
    `gemini-3-flash-preview`.

### Interactive examples

These additional conventions apply to `input()`-based chat loops:

-   Wrap `receive_steps()` in `try/except asyncio.CancelledError` that
    calls `conversation.cancel()`.
-   End with `os._exit(0)` and the standard CPython stdin-thread
    comment.
-   Use `cli_utils.print_cli_header()`, `cli_utils.INPUT_PROMPT`, and
    `cli_utils.GOODBYE_MSG` for consistent UI chrome.
