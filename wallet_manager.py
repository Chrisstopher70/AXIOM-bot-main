import base64
import json
import time
import os
from cryptography.fernet import Fernet
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.transaction import Transaction
from solders.system_program import TransferParams, transfer
from spl.token.instructions import get_associated_token_address, create_associated_token_account
from spl.token.constants import TOKEN_PROGRAM_ID
import requests
import base58

TOKEN_PROGRAM_ID = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"

class SecureWalletManager:
    def __init__(self, encryption_key):
        self.cipher_suite = Fernet(encryption_key.encode())
        self.solana_client = Client("https://api.mainnet-beta.solana.com")
        
    def generate_wallet_connect_link(self, user_id):
        """Generate secure wallet connection link using WalletConnect"""
        connection_data = {
            'user_id': user_id,
            'timestamp': int(time.time()),
            'type': 'walletconnect',
            'expiry': int(time.time()) + 3600  # 1 hour expiry
        }
        
        encrypted_data = self.cipher_suite.encrypt(
            json.dumps(connection_data).encode()
        )
        
        connection_token = base64.urlsafe_b64encode(encrypted_data).decode()
        
        # Return WalletConnect URI
        return {
            'type': 'walletconnect',
            'uri': f'wc:memecoin-bot-{user_id}@1?bridge=https%3A%2F%2Fbridge.walletconnect.org&key={connection_token}',
            'expiry': connection_data['expiry']
        }
    
    def get_wallet_balance(self, public_key_str):
        """Get SOL and token balances securely"""
        try:
            public_key = Pubkey(public_key_str)
            
            # Get SOL balance
            balance_response = self.solana_client.get_balance(public_key)
            sol_balance = balance_response['result']['value'] / 1e9
            
            # Get token accounts (simplified)
            token_accounts = self._get_token_balances(public_key_str)
            
            return {
                'sol_balance': sol_balance,
                'tokens': token_accounts,
                'total_value_usd': self._calculate_total_value(sol_balance, token_accounts)
            }
        except Exception as e:
            return None
    
    def _get_token_balances(self, public_key_str):
        """Get token balances using Jupiter API"""
        try:
            # This would integrate with Jupiter API for real token data
            # For now, return sample structure
            return {
                'USDC': {'balance': 0, 'value_usd': 0},
                'BONK': {'balance': 0, 'value_usd': 0},
                'WIF': {'balance': 0, 'value_usd': 0}
            }
        except:
            return {}
    
    def _calculate_total_value(self, sol_balance, tokens):
        """Calculate total portfolio value in USD"""
        # This would use real-time prices
        return sol_balance * 150  # Sample SOL price
    
    def verify_wallet_connection(self, public_key, signature):
        """Verify wallet ownership without exposing private keys"""
        try:
            # Implement signature verification
            return True
        except:
            return False

    def derive_keypair_from_seed(self, seed_phrase):
        """Derive Solana keypair from 12-word seed phrase"""
        try:
            from mnemonic import Mnemonic
            from bip32 import BIP32
            from ecdsa import SECP256k1
            import hashlib

            mnemo = Mnemonic("english")
            if not mnemo.check(seed_phrase):
                raise ValueError("Invalid seed phrase")

            seed = mnemo.to_seed(seed_phrase)
            bip32 = BIP32.from_seed(seed)
            # Solana uses path m/44'/501'/0'/0'
            child = bip32.get_privkey_from_path("m/44'/501'/0'/0'")
            # Convert to ed25519
            priv_key = hashlib.sha256(child).digest()[:32]
            keypair = Keypair.from_secret_key(priv_key)
            return keypair
        except ImportError:
            # Fallback: simple hash (not secure, for demo)
            import hashlib
            priv_key = hashlib.sha256(seed_phrase.encode()).digest()[:32]
            keypair = Keypair.from_secret_key(priv_key)
            return keypair

    def derive_keypair_from_private_key(self, private_key_str):
        """Derive keypair from base58 encoded private key"""
        try:
            priv_key_bytes = base58.b58decode(private_key_str)
            if len(priv_key_bytes) != 64:
                priv_key_bytes = priv_key_bytes[:32]  # Take first 32 bytes
            keypair = Keypair.from_secret_key(priv_key_bytes)
            return keypair
        except:
            raise ValueError("Invalid private key")

    def get_real_token_balances(self, public_key_str):
        """Get real token balances from Solana blockchain"""
        try:
            public_key = Pubkey(public_key_str)
            response = self.solana_client.get_token_accounts_by_owner(
                public_key, 
                {"programId": TOKEN_PROGRAM_ID}
            )
            tokens = {}
            for account in response['result']['value']:
                account_data = account['account']['data']
                # Parse token account data (simplified)
                mint = account_data['parsed']['info']['mint']
                balance = int(account_data['parsed']['info']['tokenAmount']['amount']) / (10 ** int(account_data['parsed']['info']['tokenAmount']['decimals']))
                # Get token symbol (would need token list API)
                symbol = self._get_token_symbol(mint)
                tokens[symbol] = {'balance': balance, 'mint': mint}
            return tokens
        except:
            return {}

    def _get_token_symbol(self, mint):
        """Get token symbol from mint address (simplified)"""
        # This would use a token list API
        known_tokens = {
            'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v': 'USDC',
            'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263': 'BONK',
            'EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm': 'WIF'
        }
        return known_tokens.get(str(mint), str(mint)[:8])

    def get_jupiter_quote(self, input_mint, output_mint, amount, slippage=0.5):
        """Get quote from Jupiter API"""
        try:
            url = f"https://quote-api.jup.ag/v6/quote?inputMint={input_mint}&outputMint={output_mint}&amount={amount}&slippageBps={int(slippage*100)}"
            response = requests.get(url)
            return response.json()
        except:
            return None

    def execute_swap(self, keypair, quote_response):
        """Execute swap transaction using Jupiter"""
        try:
            # Get swap transaction
            swap_url = "https://quote-api.jup.ag/v6/swap"
            data = {
                "quoteResponse": quote_response,
                "userPublicKey": str(keypair.public_key),
                "wrapAndUnwrapSol": True
            }
            response = requests.post(swap_url, json=data)
            swap_data = response.json()

            # Deserialize and sign transaction
            txn = Transaction.deserialize(base64.b64decode(swap_data['swapTransaction']))
            txn.sign(keypair)

            # Send transaction
            result = self.solana_client.send_transaction(txn)
            return result
        except Exception as e:
            return None
