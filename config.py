import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Bot Configuration
    BOT_TOKEN = os.getenv('BOT_TOKEN', '7926468357:AAGTB_iYfSR28VhYpLcVaVZ8fQ99M4qsAHM')
    ADMIN_ID = int(os.getenv('ADMIN_ID', '6489177483'))
    
    # Solana Configuration
    SOLANA_RPC_URL = os.getenv('SOLANA_RPC_URL', 'https://api.mainnet-beta.solana.com')
    JUPITER_API_URL = 'https://quote-api.jup.ag/v6'
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///memecoin_bot.db')
    
    # Security
    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', 'CEdwY5HgxX_CmJqGh7oCdQ3jimNimyPO-1F86eQclQs=')
