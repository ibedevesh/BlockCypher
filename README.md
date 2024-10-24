# Bitcoin Address Information Tool

This Python tool retrieves and displays detailed information about a **Bitcoin address** using the **BlockCypher API**. It provides insights into the address’s final balance, transactions, and distinguishes between **sent** and **received transactions**.

---

## Features

- **Fetch Bitcoin address information**: Balance, total BTC received/sent, and number of transactions.
- **Analyze transactions**: 
  - Identify transactions where the address **sends or receives BTC**.
  - Display **top senders and recipients** in transactions.
- **Handle pagination**: Use batching for large datasets by limiting API requests.

---

## Prerequisites

1. **Python 3.x** installed on your machine.
2. Install the required dependencies:
   ```bash
   pip install requests
