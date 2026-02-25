# Binance Futures Trading Bot

A production-ready trading bot for Binance Futures Testnet (USDT-M) with CLI and web interface.

## Setup

### Prerequisites
- Python 3.7 or higher
- Internet connection
- Binance Futures Testnet account

### Installation Steps

1. **Clone or download this project**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Get API credentials**
   - Go to [Binance Futures Testnet](https://testnet.binancefuture.com/)
   - Login with GitHub or Google account
   - Navigate to API Management
   - Generate API Key and Secret Key
   - Copy both keys

4. **Configure environment**
```bash
# Windows
Copy-Item .env.example .env

# Linux/Mac
cp .env.example .env
```

Edit `.env` file and add your credentials:
```
BINANCE_API_KEY=your_api_key_here
BINANCE_SECRET_KEY=your_secret_key_here
BASE_URL=https://testnet.binancefuture.com
```

5. **Get testnet funds**
   - Login to [Binance Futures Testnet](https://testnet.binancefuture.com/)
   - Click "Get Test Funds" button
   - Receive free testnet USDT

## How to Run

### Quick Test (Copy & Paste)

Test the bot with these ready-to-use commands:

```bash
# Test 1: MARKET Buy Order
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.002

# Test 2: MARKET Sell Order
python cli.py --symbol BTCUSDT --side SELL --type MARKET --quantity 0.002

# Test 3: LIMIT Buy Order (adjust price to current market)
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.002 --price 94000

# Test 4: LIMIT Sell Order (adjust price to current market)
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.002 --price 96000

# Test 5: Different Symbol - Ethereum
python cli.py --symbol ETHUSDT --side BUY --type MARKET --quantity 0.05

# Test 6: Different Symbol - Binance Coin
python cli.py --symbol BNBUSDT --side BUY --type MARKET --quantity 0.2
```

### CLI Interface

**MARKET Order - BUY**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.002
```

**MARKET Order - SELL**
```bash
python cli.py --symbol BTCUSDT --side SELL --type MARKET --quantity 0.002
```

**LIMIT Order - BUY**
```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.002 --price 94000
```

**LIMIT Order - SELL**
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.002 --price 96000
```

### Web Interface

1. **Start the server**
```bash
python app.py
```

2. **Open browser**
   - Navigate to `http://localhost:5000`
   - Fill in the form
   - Click "Place Order"

## Expected Output

### CLI Output
```
==================================================
ORDER REQUEST SUMMARY
==================================================
Symbol:       BTCUSDT
Side:         BUY
Order Type:   MARKET
Quantity:     0.002
==================================================

==================================================
ORDER RESPONSE DETAILS
==================================================
Order ID:     12345678
Status:       NEW
Symbol:       BTCUSDT
Side:         BUY
Type:         MARKET
Quantity:     0.002
Executed Qty: 0.002
==================================================

SUCCESS: Order placed successfully!
```

### Log File
All requests and responses are logged to `bot.log`:
```
2026-02-25 21:47:30,730 - INFO - API Request - Endpoint: /fapi/v1/order, Params: {...}
2026-02-25 21:47:31,412 - INFO - API Response - Status: 200, Data: {...}
```

## Assumptions

### Technical Assumptions
- Python 3.7+ is installed
- User has internet access
- Binance Futures Testnet is accessible
- User can create and edit `.env` files

### Trading Assumptions
- Minimum order value: $100 USD
- BTCUSDT quantity: minimum 0.002 (≈$190 at $95k)
- ETHUSDT quantity: minimum 0.05 (≈$150 at $3k)
- Price precision: 2 decimal places
- Quantity precision: 3 decimals for BTC/ETH, 1 decimal for others
- LIMIT prices must be within ~10% of current market price
- All orders use GTC (Good Till Cancel) time in force

### API Assumptions
- Testnet API endpoint: `https://testnet.binancefuture.com`
- API uses HMAC SHA256 signature authentication
- Timestamp must be within server time window
- Rate limits are not enforced on testnet (but respected)

### Order Type Support
- MARKET orders: Supported (executes immediately)
- LIMIT orders: Supported (executes at specified price)
- STOP orders: Not implemented (requires Algo Order API)

## Features

- MARKET & LIMIT order types
- BUY & SELL operations
- CLI with argparse validation
- Web UI with Flask
- HMAC SHA256 authentication
- Input validation
- File logging (bot.log)
- Error handling
- Automatic precision formatting
- Environment-based configuration

## Project Structure

```
trading_bot/
├── bot/
│   ├── client.py           # API client with HMAC signature
│   ├── orders.py           # Order service layer
│   ├── validators.py       # Input validation
│   └── logging_config.py   # Logging setup
├── templates/
│   └── index.html          # Web UI
├── static/
│   ├── style.css           # UI styling
│   └── script.js           # Frontend logic
├── cli.py                  # CLI interface
├── app.py                  # Flask web server
├── requirements.txt        # Dependencies
├── .env.example           # Environment template
└── README.md
```

## Troubleshooting

### "Missing API credentials"
- Ensure `.env` file exists in project root
- Verify API keys are correctly copied (no extra spaces)

### "Margin is insufficient"
- Get testnet funds from the testnet website
- Click "Get Test Funds" button

### "Order's notional must be no smaller than 100"
- Increase quantity (minimum $100 order value)
- For BTCUSDT: use 0.002 or higher

### "Limit price can't be lower/higher than X"
- Check current market price on testnet website
- Use price within 10% of market price

### "Invalid symbol"
- Use valid symbols: BTCUSDT, ETHUSDT, BNBUSDT
- Symbols are auto-converted to uppercase

## Valid Trading Pairs

- BTCUSDT (Bitcoin) - Min: 0.002
- ETHUSDT (Ethereum) - Min: 0.05
- BNBUSDT (Binance Coin) - Min: 0.2
- ADAUSDT (Cardano) - Min: 100
- SOLUSDT (Solana) - Min: 1
- XRPUSDT (Ripple) - Min: 100

## Test Data Examples

### Quick Copy-Paste Test Commands

```bash
# MARKET Orders (Execute immediately)
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.002
python cli.py --symbol ETHUSDT --side BUY --type MARKET --quantity 0.05
python cli.py --symbol BNBUSDT --side SELL --type MARKET --quantity 0.2

# LIMIT Orders (Check current price first at testnet.binancefuture.com)
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.002 --price 94000
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.05 --price 3500
python cli.py --symbol BNBUSDT --side BUY --type LIMIT --quantity 0.2 --price 600
```

### Test Scenarios

**Scenario 1: Basic Trading Flow**
```bash
# 1. Buy BTC at market price
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.002

# 2. Sell BTC at market price
python cli.py --symbol BTCUSDT --side SELL --type MARKET --quantity 0.002
```

**Scenario 2: Limit Order Strategy**
```bash
# 1. Place buy limit order below market
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.002 --price 93000

# 2. Place sell limit order above market
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.002 --price 97000
```

**Scenario 3: Multi-Asset Trading**
```bash
# Buy different cryptocurrencies
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.002
python cli.py --symbol ETHUSDT --side BUY --type MARKET --quantity 0.05
python cli.py --symbol BNBUSDT --side BUY --type MARKET --quantity 0.2
```

### View Logs
```bash
# Windows
type bot.log

# Linux/Mac
cat bot.log

# View last 20 lines
Get-Content bot.log -Tail 20  # Windows
tail -20 bot.log              # Linux/Mac
```

## Notes

- This is for TESTNET only (fake money)
- Testnet funds are unlimited and free
- All logs saved to `bot.log`
- Symbols automatically uppercased
- Precision automatically formatted
