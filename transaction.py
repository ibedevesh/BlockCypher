import requests
import json
from datetime import datetime

def get_address_info(address, before=None, limit=50):
    url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/full?limit={limit}"
    if before:
        url += f"&before={before}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def satoshi_to_btc(satoshi):
    return satoshi / 1e8

def safe_get(dct, *keys, default=None):
    for key in keys:
        try:
            dct = dct[key]
        except (KeyError, TypeError):
            return default
    return dct

def print_address_info(address):
    address_data = get_address_info(address)
    if not address_data:
        print(f"Unable to fetch data for address: {address}")
        return

    print(f"Address: {address}")
    print(f"Final Balance: {satoshi_to_btc(address_data['final_balance']):.8f} BTC")
    print(f"Total Received: {satoshi_to_btc(address_data['total_received']):.8f} BTC")
    print(f"Total Sent: {satoshi_to_btc(address_data['total_sent']):.8f} BTC")
    print(f"Number of Transactions: {address_data['n_tx']}")

    print("\nTransactions:")
    sent_transactions = []
    received_transactions = []
    before = None
    max_batches = 10  # Limit the number of API calls

    for _ in range(max_batches):
        transactions = get_address_info(address, before)['txs']
        if not transactions:
            break

        for tx in transactions:
            tx_time = tx['received']
            tx_id = tx['hash']
            
            inputs = tx['inputs']
            outputs = tx['outputs']
            
            is_sending = any(address in (safe_get(input, 'addresses') or []) for input in inputs)
            
            if is_sending:
                amount_sent = sum(safe_get(output, 'value', default=0) for output in outputs 
                                  if address not in (safe_get(output, 'addresses') or []))
                recipients = [addr for output in outputs 
                              for addr in (safe_get(output, 'addresses') or [])
                              if addr != address]
                sent_transactions.append((tx_time, amount_sent, recipients, tx_id))
            else:
                amount_received = sum(safe_get(output, 'value', default=0) for output in outputs 
                                      if address in (safe_get(output, 'addresses') or []))
                senders = [addr for input in inputs 
                           for addr in (safe_get(input, 'addresses') or [])]
                received_transactions.append((tx_time, amount_received, senders, tx_id))

        before = transactions[-1]['block_height']
        
        if sent_transactions:
            break

    print("\nSent Transactions:")
    for tx_time, amount, recipients, tx_id in sent_transactions[:10]:
        print(f"Transaction ID: {tx_id}")
        print(f"Sent: {satoshi_to_btc(amount):.8f} BTC on {tx_time}")
        print(f"  To: {', '.join(str(r) for r in recipients[:3])}{'...' if len(recipients) > 3 else ''}")
        print()

    print("\nReceived Transactions:")
    for tx_time, amount, senders, tx_id in received_transactions[:10]:
        print(f"Transaction ID: {tx_id}")
        print(f"Received: {satoshi_to_btc(amount):.8f} BTC on {tx_time}")
        print(f"  From: {', '.join(str(s) for s in senders[:3])}{'...' if len(senders) > 3 else ''}")
        print()

def main():
    address = input("Enter a Bitcoin address: ")
    print_address_info(address)

if __name__ == "__main__":
    main()
