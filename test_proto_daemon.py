#!/usr/bin/env python3
import requests
import time
import sys

BASE_URL = "http://localhost:8000"

def test_status():
    print("Testing /status...")
    resp = requests.get(f"{BASE_URL}/status")
    print(resp.json())
    assert resp.status_code == 200

def test_list_agents():
    print("Testing /agents...")
    resp = requests.get(f"{BASE_URL}/agents")
    print(resp.json())
    assert resp.status_code == 200
    return resp.json()

def test_handover():
    print("Testing /handover/AliceToBob...")
    resp = requests.post(f"{BASE_URL}/handover/AliceToBob")
    print(resp.json())
    assert resp.status_code == 200

def test_memory():
    print("Testing /memory/write...")
    payload = {
        "key": "test_key",
        "value": "test_value",
        "embedding": [0.1] * 384
    }
    resp = requests.post(f"{BASE_URL}/memory/write", json=payload)
    print(resp.json())
    assert resp.status_code == 200

    print("Testing /memory/query...")
    query = {
        "embedding": [0.1] * 384,
        "top_k": 1
    }
    resp = requests.post(f"{BASE_URL}/memory/query", json=query)
    print(resp.json())
    assert resp.status_code == 200

if __name__ == "__main__":
    try:
        test_status()
        agents_before = test_list_agents()
        test_handover()
        agents_after = test_list_agents()
        test_memory()
        print("\n✅ All daemon tests passed!")
    except Exception as e:
        print(f"\n❌ Tests failed: {e}")
        sys.exit(1)
