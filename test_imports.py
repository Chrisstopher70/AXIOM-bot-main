import asyncio
from trading import MemecoinTrader
from wallet_manager import SecureWalletManager
from cryptography.fernet import Fernet

async def test():
    # Generate a valid Fernet key
    key = Fernet.generate_key()
    wm = SecureWalletManager(key.decode())
    trader = MemecoinTrader(wm)

    print('Testing get_token_mint for BONK:', trader.get_token_mint('BONK'))

    print('Testing get_real_balance with dummy user_id')
    balance = await trader.get_real_balance('dummy_user')
    print('Balance:', balance)

    print('Testing buy_token with dummy data')
    result = await trader.buy_token('dummy_user', 'BONK', 0.01)
    print('Buy token result:', result)

    print('Testing sell_token with dummy data')
    result = await trader.sell_token('dummy_user', 'BONK', 10)
    print('Sell token result:', result)

if __name__ == '__main__':
    asyncio.run(test())
