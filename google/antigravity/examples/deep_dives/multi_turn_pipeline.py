# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Multi-turn conversation with back-to-back sends.

Demonstrates that Conversation.send() safely handles being called
multiple times without manually draining receive_steps() between
turns. The SDK automatically drains any pending steps into the
conversation history before sending the next message.

This is especially useful for scripted pipelines where you want to
fire-and-forget a sequence of prompts and only inspect the final
result.

Demonstrates:
- Back-to-back send() calls without explicit receive_steps() drain.
- Automatic history preservation: all turns' responses are recorded.
- History inspection via conversation.history and turn_count.

Run:
    python multi_turn_pipeline.py

Example output::

  ============================================================
    Multi-turn pipeline: back-to-back sends
  ============================================================

    >>> What is the capital of France?

    >>> What is the population of that city?

    >>> Name one famous landmark there.
    <<< The Eiffel Tower is one of the most famous landmarks in Paris.

  ============================================================
    History (3 turns, 7 steps)
  ============================================================
    1. [USER] What is the capital of France?
    2. [MODEL] The capital of France is Paris.
    3. [USER] What is the population of that city?
    4. [MODEL] The population of Paris is approximately 2.1 million people.
    5. [USER] Name one famous landmark there.
    6. [MODEL] The Eiffel Tower is one of the most famous landmarks in Paris.
"""

import asyncio
import logging

from google.antigravity.agent import Agent
from google.antigravity.connections.local.local_connection_config import LocalAgentConfig


async def main() -> None:
  logging.basicConfig(level=logging.WARNING)

  config = LocalAgentConfig(
      system_instructions=(
          "You are a concise assistant. Answer in one sentence."
      ),
  )

  agent = Agent(config)

  async with agent:
    conv = agent.conversation

    # --- Pipeline: send three prompts back-to-back ---
    prompts = [
        "What is the capital of France?",
        "What is the population of that city?",
        "Name one famous landmark there.",
    ]

    print("=" * 60)
    print("  Multi-turn pipeline: back-to-back sends")
    print("=" * 60)

    for prompt in prompts:
      print(f"\n  >>> {prompt}")
      # Each send() automatically drains the previous turn's response
      # into conversation.history before sending.
      await conv.send(prompt)

    # Drain the final turn.
    async for step in conv.receive_steps():
      if step.content:
        print(f"  <<< {step.content}")

    # --- Inspect history ---
    print(f"\n{'=' * 60}")
    print(f"  History ({conv.turn_count} turns, {len(conv.history)} steps)")
    print(f"{'=' * 60}")

    for i, step in enumerate(conv.history, 1):
      label = step.source.name
      text = step.content or "(no content)"
      print(f"  {i}. [{label}] {text}")


if __name__ == "__main__":
  asyncio.run(main())
