"""Check which Nebius Token Factory models support Chat and Responses APIs.
Runs all models in parallel. Prints markdown output."""

import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import APIError, OpenAI

load_dotenv()
api_key = os.getenv("NEBIUS_API_KEY")
if not api_key:
    raise RuntimeError("Set NEBIUS_API_KEY in your environment or .env file.")

client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=api_key,
    timeout=30.0,
)


@dataclass
class ModelResult:
    id: str
    chat_ok: bool
    chat_ms: float
    responses_ok: bool
    responses_ms: float


def check_chat(model: str) -> tuple[bool, float]:
    start = time.perf_counter()
    try:
        client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=5,
        )
        elapsed = (time.perf_counter() - start) * 1000
        print(f"    {model} chat OK in {elapsed:.0f}ms")
        return True, elapsed
    except APIError as e:
        elapsed = (time.perf_counter() - start) * 1000
        print(f"    {model} chat FAIL in {elapsed:.0f}ms: {e.message or e}")
        return False, elapsed
    except Exception as e:
        elapsed = (time.perf_counter() - start) * 1000
        print(f"    {model} chat FAIL in {elapsed:.0f}ms: {e}")
        return False, elapsed


def check_responses(model: str) -> tuple[bool, float]:
    start = time.perf_counter()
    try:
        client.responses.create(
            model=model,
            input="Hi",
            max_output_tokens=5,
        )
        elapsed = (time.perf_counter() - start) * 1000
        print(f"    {model} responses OK in {elapsed:.0f}ms")
        return True, elapsed
    except APIError as e:
        elapsed = (time.perf_counter() - start) * 1000
        print(f"    {model} responses FAIL in {elapsed:.0f}ms: {e.message or e}")
        return False, elapsed
    except Exception as e:
        elapsed = (time.perf_counter() - start) * 1000
        print(f"    {model} responses FAIL in {elapsed:.0f}ms: {e}")
        return False, elapsed


def check_model(model: str) -> ModelResult:
    print(f"  {model} ...")
    chat_ok, chat_ms = check_chat(model)
    responses_ok, responses_ms = check_responses(model)
    return ModelResult(model, chat_ok, chat_ms, responses_ok, responses_ms)


start_run = time.perf_counter()

models = [m.id for m in client.models.list() if "embedding" not in m.id.lower()]
models.sort(key=str.lower)
print(f"Checking {len(models)} model(s) in parallel...")

results: list[ModelResult] = []
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(check_model, m) for m in models]
    for future in as_completed(futures):
        results.append(future.result())

results.sort(key=lambda r: r.id.lower())
total_s = time.perf_counter() - start_run

model_width = max(len(r.id) for r in results)
status_width = 5

print()
print(f"| {'Model':<{model_width}} | {'Chat':^{status_width}} | {'Responses':^{status_width}} |")
print(f"| {'-' * model_width} | {'-' * status_width}: | {'-' * status_width}: |")

for r in results:
    chat_status = "✅" if r.chat_ok else "❌"
    resp_status = "✅" if r.responses_ok else "❌"
    print(
        f"| {r.id:<{model_width}} | "
        f"{chat_status:^{status_width}} | "
        f"{resp_status:^{status_width}} |"
    )

chat = sum(1 for r in results if r.chat_ok)
resp = sum(1 for r in results if r.responses_ok)
print()
print(f"**Summary:** {chat}/{len(results)} chat, {resp}/{len(results)} responses")
print(f"**Total time:** {total_s:.1f}s")
