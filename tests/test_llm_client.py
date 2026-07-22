"""
Standalone integration test for LLMClient using real Mistral API.
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.rag.llm_client import LLMClient


def run_tests():
    passed = 0
    failed = 0
    total = 7

    def record_result(name, action):
        nonlocal passed, failed
        try:
            action()
            print(f"[PASS] {name}")
            passed += 1
        except Exception as e:
            print(f"[FAIL] {name}: {e}")
            failed += 1

    # TEST 1: Initialize LLMClient
    client = None
    def test1():
        nonlocal client
        client = LLMClient()
        if client is None or client.llm is None:
            raise AssertionError("LLMClient failed to initialize.")
    record_result("LLMClient initialized", test1)

    # TEST 2: health_check()
    def test2():
        status = client.health_check()
        if status is not True:
            raise AssertionError(f"Expected health_check() to return True, got {status}")
    record_result("Health check", test2)

    prompt = "Reply with exactly one word: SUCCESS"

    # TEST 3: generate()
    resp_text = ""
    def test3():
        nonlocal resp_text
        resp_text = client.generate(prompt)
        if not isinstance(resp_text, str):
            raise AssertionError(f"Expected string return type, got {type(resp_text)}")
        if not resp_text.strip():
            raise AssertionError("Returned response string is empty.")
    record_result("Generate response", test3)

    # TEST 4: Multiple requests
    def test4():
        r1 = client.generate(prompt)
        r2 = client.generate(prompt)
        if not isinstance(r1, str) or not r1.strip():
            raise AssertionError("First response in multiple requests is invalid.")
        if not isinstance(r2, str) or not r2.strip():
            raise AssertionError("Second response in multiple requests is invalid.")
    record_result("Multiple requests", test4)

    # TEST 5: Validation prompt
    def test5():
        for invalid in [None, "", "      ", 123]:
            try:
                client.generate(invalid)
                raise AssertionError(f"Expected ValueError for generate({invalid})")
            except ValueError:
                pass
            except Exception as e:
                raise AssertionError(f"Expected ValueError for generate({invalid}), got {type(e)}")
    record_result("Validation prompt", test5)

    # TEST 6: Validation invalid types
    def test6():
        for invalid in [[], {}]:
            try:
                client.generate(invalid)
                raise AssertionError(f"Expected ValueError for generate({invalid})")
            except ValueError:
                pass
            except Exception as e:
                raise AssertionError(f"Expected ValueError for generate({invalid}), got {type(e)}")
    record_result("Validation invalid types", test6)

    # TEST 7: Verify return type
    def test7():
        response = client.generate(prompt)
        if response is None:
            raise AssertionError("generate() returned None.")
        if not isinstance(response, str):
            raise AssertionError(f"Expected str, got {type(response)}")
        if type(response).__name__ in ["AIMessage", "HumanMessage", "BaseMessage"]:
            raise AssertionError("generate() returned a LangChain message object instead of str.")
    record_result("Return type", test7)

    # Summary
    print("\n=====================================")
    print(f"Total Tests : {total}")
    print(f"Passed      : {passed}")
    print(f"Failed      : {failed}")
    print("=====================================\n")

    if passed == total:
        print("LLMClient integration tests completed successfully.")


if __name__ == "__main__":
    run_tests()
