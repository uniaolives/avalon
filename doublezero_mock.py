#!/usr/bin/env python3
import sys
import json
import random

def main():
    if len(sys.argv) < 2:
        print("Usage: doublezero <command>")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "keygen":
        print("Generating new identity...")
        # Simulates key generation
    elif cmd == "address":
        print("96AfeBT6UqUmREmPeFZxw6PbLrbfET51NxBFCCsVAnek")
    elif cmd == "latency":
        print(" pubkey                                       | name      | ip             | min      | max      | avg      | reachable")
        print(" 96AfeBT6UqUmREmPeFZxw6PbLrbfET51NxBFCCsVAnek | la2-dz01  | 207.45.216.134 |   0.38ms |   0.45ms |   0.42ms | true")
        print(" CCTSmqMkxJh3Zpa9gQ8rCzhY7GiTqK7KnSLBYrRriuan | ny5-dz01  | 64.86.249.22   |  68.81ms |  68.87ms |  68.85ms | true")
        print(" BX6DYCzJt3XKRc1Z3N8AMSSqctV6aDdJryFMGThNSxDn | ty2-dz01  | 180.87.154.78  | 112.16ms | 112.25ms | 112.22ms | true")
    elif cmd == "status":
        print("Status: up")
        print("Network: mainnet-beta")
        print("Interface: doublezero0")
    elif cmd == "disconnect":
        print("Disconnecting...")
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
