from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram import Update
import time

class SecureWalletHandlers:
    def __init__(self, wallet_manager):
        self.wallet_manager = wallet_manager
        
    async def connect_solflare_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle Solflare wallet connection"""
        query = update.callback_query
        await query.answer()
        
        user_id = str(query.from_user.id)
        
        keyboard = [[InlineKeyboardButton("🔙 Main Menu", callback_data='menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"☀️ **Solflare Wallet Connection**\n\n"
            f"🔗 **Connection Method:** Mobile App\n\n"
            f"**Steps:**\n"
            f"1. Open Solflare mobile app\n"
            f"2. Navigate to WalletConnect\n"
            f"3. Scan the QR code\n"
            f"4. Approve the connection\n\n"
            f"⚡ **Status:** Ready for connection",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
    async def connect_walletconnect_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle WalletConnect universal connection"""
        query = update.callback_query
        await query.answer()
        
        user_id = str(query.from_user.id)
        connection_info = self.wallet_manager.generate_wallet_connect_link(user_id)
        
        keyboard = [[InlineKeyboardButton("🔙 Main Menu", callback_data='menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"🔗 **WalletConnect Universal**\n\n"
            f"**Compatible Wallets:**\n"
            f"• Phantom\n"
            f"• Solflare\n"
            f"• Trust Wallet\n"
            f"• Coin98\n"
            f"• And many more...\n\n"
            f"**Connection URI:**\n"
            f"`{connection_info['uri'][:60]}...`\n\n"
            f"⏰ **Expires:** <t:{connection_info['expiry']}:R>",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
    async def sell_tokens_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle token selling interface"""
        query = update.callback_query
        await query.answer()
        
        keyboard = [
            [InlineKeyboardButton("🪙 Sell BONK", callback_data='sell_bonk')],
            [InlineKeyboardButton("🐶 Sell WIF", callback_data='sell_wif')],
            [InlineKeyboardButton("🐸 Sell PEPE", callback_data='sell_pepe')],
            [InlineKeyboardButton("🔙 Back", callback_data='trade')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🔴 **Sell Tokens**\n\n"
            "Select a token to sell:",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
    async def portfolio_performance_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show portfolio performance analytics"""
        query = update.callback_query
        await query.answer()
        
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='portfolio')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        performance_text = """
📈 **Portfolio Performance**

**📊 24h Performance:** `+5.23%`
**📊 7d Performance:** `+12.45%`
**📊 30d Performance:** `+34.67%`

**💰 Total P&L:** `+$1,234.56`
**💎 Best Performer:** `BONK (+15.3%)`
**📉 Worst Performer:** `WIF (-2.1%)`

**📋 Top Holdings:**
1. **SOL:** 45.2% of portfolio
2. **BONK:** 32.1% of portfolio
3. **WIF:** 22.7% of portfolio
        """
        
        await query.edit_message_text(
            performance_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
    async def portfolio_holdings_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show detailed holdings"""
        query = update.callback_query
        await query.answer()
        
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='portfolio')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        holdings_text = """
📊 **Detailed Holdings**

**💎 SOL:** `2.345 SOL` ($351.75)
**🪙 BONK:** `1,234,567 BONK` ($234.56)
**🐶 WIF:** `456 WIF` ($123.45)
**🐸 PEPE:** `789,012 PEPE` ($67.89)

**💰 Total Value:** $777.65
**📈 24h Change:** +5.23%
        """
        
        await query.edit_message_text(
            holdings_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
