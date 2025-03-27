# blockchain_viewer.py
import pickle
from datetime import datetime

def view_blockchain():
    try:
        with open('blockchain_contract.txt', 'rb') as f:
            blockchain = pickle.load(f)
            
            print("\nBLOCKCHAIN CONTENTS")
            print("==================")
            
            for block in blockchain.chain:
                print(f"\nBlock #{block.index}")
                print(f"Timestamp: {datetime.fromtimestamp(block.timestamp)}")
                print(f"Previous Hash: {block.previous_hash}")
                print(f"Current Hash: {block.hash}")
                print(f"Nonce: {block.nonce}")
                
                print("\nTransactions:")
                for tx in block.transactions:
                    if "#" in tx:
                        parts = tx.split("#")
                        print(f"  Product ID: {parts[0]}")
                        print(f"  Name: {parts[1]}")
                        print(f"  Company: {parts[2]}")
                        print(f"  Address: {parts[3]}")
                        print(f"  Timestamp: {parts[4]}")
                        print(f"  Signature: {parts[5][:20]}...")
                    else:
                        print(f"  Raw TX: {tx}")
                
                print("-" * 60)

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    view_blockchain()