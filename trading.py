import asyncio
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.transaction import Transaction
from spl.token.instructions import get_associated_token_address
from spl.token.constants import TOKEN_PROGRAM_ID

TOKEN_PROGRAM_ID = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
import requests
import base58
from wallet_manager import SecureWalletManager

class MemecoinTrader:
    def __init__(self, wallet_manager):
        self.wallet_manager = wallet_manager
        self.solana_client = wallet_manager.solana_client

    def get_keypair_from_encrypted(self, encrypted_private_key):
        """Decrypt and get keypair from encrypted private key"""
        decrypted = self.wallet_manager.cipher_suite.decrypt(encrypted_private_key.encode())
        return Keypair.from_secret_key(decrypted)

    async def buy_token(self, user_id, token_symbol, amount_sol, slippage=0.5):
        """Buy memecoin using SOL"""
        try:
            if user_id not in self.wallet_manager.user_wallets:
                return {"error": "Wallet not connected"}

            wallet_info = self.wallet_manager.user_wallets[user_id]
            keypair = self.get_keypair_from_encrypted(wallet_info['encrypted_private_key'])

            # Get token mint address
            token_mint = self.get_token_mint(token_symbol)
            if not token_mint:
                return {"error": "Token not found"}

            # Convert SOL to lamports
            amount_lamports = int(amount_sol * 1e9)

            # Get quote from Jupiter
            quote = self.wallet_manager.get_jupiter_quote(
                "So11111111111111111111111111111111111111112",  # SOL mint
                token_mint,
                amount_lamports,
                slippage
            )

            if not quote:
                return {"error": "Failed to get quote"}

            # Execute swap
            result = self.wallet_manager.execute_swap(keypair, quote)

            if result:
                return {
                    "success": True,
                    "tx_hash": result['result'],
                    "amount": amount_sol,
                    "token": token_symbol
                }
            else:
                return {"error": "Transaction failed"}

        except Exception as e:
            return {"error": str(e)}

    async def sell_token(self, user_id, token_symbol, amount_tokens, slippage=0.5):
        """Sell memecoin for SOL"""
        try:
            if user_id not in self.wallet_manager.user_wallets:
                return {"error": "Wallet not connected"}

            wallet_info = self.wallet_manager.user_wallets[user_id]
            keypair = self.get_keypair_from_encrypted(wallet_info['encrypted_private_key'])

            # Get token mint address
            token_mint = self.get_token_mint(token_symbol)
            if not token_mint:
                return {"error": "Token not found"}

            # Get token decimals
            decimals = self.get_token_decimals(token_mint)
            amount_lamports = int(amount_tokens * (10 ** decimals))

            # Get quote from Jupiter
            quote = self.wallet_manager.get_jupiter_quote(
                token_mint,
                "So11111111111111111111111111111111111111112",  # SOL mint
                amount_lamports,
                slippage
            )

            if not quote:
                return {"error": "Failed to get quote"}

            # Execute swap
            result = self.wallet_manager.execute_swap(keypair, quote)

            if result:
                return {
                    "success": True,
                    "tx_hash": result['result'],
                    "amount": amount_tokens,
                    "token": token_symbol
                }
            else:
                return {"error": "Transaction failed"}

        except Exception as e:
            return {"error": str(e)}

    def get_token_mint(self, symbol):
        """Get token mint address from symbol"""
        token_map = {
            'BONK': 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263',
            'WIF': 'EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm',
            'USDC': 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'
        }
        return token_map.get(symbol.upper())

    def get_token_decimals(self, mint):
        """Get token decimals (simplified)"""
        # In real implementation, query the token mint
        return 9  # Most memecoins use 9 decimals

    async def get_real_balance(self, user_id):
        """Get real wallet balance"""
        try:
            if user_id not in self.wallet_manager.user_wallets:
                return None

            wallet_info = self.wallet_manager.user_wallets[user_id]
            public_key = Pubkey(wallet_info['public_key'])

            # Get SOL balance
            sol_response = self.solana_client.get_balance(public_key)
            sol_balance = sol_response['result']['value'] / 1e9

            # Get token balances
            tokens = self.wallet_manager.get_real_token_balances(wallet_info['public_key'])

            return {
                'sol_balance': sol_balance,
                'tokens': tokens,
                'total_value_usd': self.calculate_total_value(sol_balance, tokens)
            }

        except Exception as e:
            return None

    def calculate_total_value(self, sol_balance, tokens):
        """Calculate total portfolio value in USD"""
        # Get current prices (simplified)
        sol_price = 150  # Sample price
        total = sol_balance * sol_price

        # Add token values (would need price API)
        for symbol, data in tokens.items():
            if symbol == 'USDC':
                total += data['balance']
            # Add other token prices here

        return total
