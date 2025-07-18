BUTTONS = {
    "ru": {
        "balance": "💰 Баланс",
        "buy_gift": "🎁 Купить подарок",
        "deposit": "💳 Депозит",
        "auto_buy": "🤖 Автопокупка",
        "history": "🕓 История",
        "notifications_on": "🔕 Не беспокоить",
        "notifications_off": "🔔 Включить уведомления",
        "language": "🌐 Язык",
        "back": "🔙 Назад",
        "cancel": "❌ Отмена",
        "next": "➡️ Вперёд",
        "prev": "⬅️ Назад",
        "auto_buy_toggle": "🔄 Вкл/Выкл автопокупку",
        "auto_buy_price": "✏️ Лимит цены",
        "auto_buy_supply": "✏️ Лимит количества",
        "auto_buy_cycles": "✏️ Кол-во циклов",
    },
    "en": {
        "balance": "💰 Balance",
        "buy_gift": "🎁 Buy gift",
        "deposit": "💳 Deposit",
        "auto_buy": "🤖 Auto-buy",
        "history": "🕓 History",
        "notifications_on": "🔕 Do not disturb",
        "notifications_off": "🔔 Enable notifications",
        "language": "🌐 Language",
        "back": "🔙 Back",
        "cancel": "❌ Cancel",
        "next": "➡️ Next",
        "prev": "⬅️ Back",
        "auto_buy_toggle": "🔄 Toggle auto-buy",
        "auto_buy_price": "✏️ Price limit",
        "auto_buy_supply": "✏️ Supply limit",
        "auto_buy_cycles": "✏️ Cycles",
    },
}

MESSAGES = {
    "ru": {
        "auto_buy_status": lambda status: f"Статус автопокупки: {'🟢 Включена' if status else '🔴 Выключена'}.",
        "auto_buy_settings": lambda user, settings: (
            f"{user.username}, твой баланс: {user.balance}⭐️\n\n"
            f"⚙️ <b>Автопокупка</b>\n"
            f"Статус: {'🟢 Включена' if settings.status else '🔴 Выключена'}\n\n"
            f"<b>Лимит цены:</b> от {settings.price_limit_from} до {settings.price_limit_to}⭐️\n"
            f"<b>Лимит количества:</b> {settings.supply_limit or 'не задан'}\n"
            f"<b>Циклов:</b> {settings.cycles}\n"
        ),
        "auto_buy_price_set": lambda price_from, price_to: f"✅ Лимит цены установлен: от {price_from} до {price_to}⭐️",
        "auto_buy_supply_set": lambda supply_limit: f"✅ Лимит количества установлен: {supply_limit}",
        "auto_buy_cycles_set": lambda cycles: f"✅ Количество циклов установлено: {cycles}",
        "auto_buy_price_prompt": "Введи лимит цены через пробел: ОТ ДО (например, 10 100)",
        "auto_buy_supply_prompt": "Введи лимит количества подарков (например, 50)",
        "auto_buy_cycles_prompt": "Введи количество циклов (например, 2). Каждый цикл — это попытка купить подарки.",
        "auto_buy_price_error": "Ошибка! Введи лимит цены через пробел: ОТ ДО (например, 10 100)",
        "auto_buy_supply_error": "Ошибка! Введи положительное число для лимита.",
        "auto_buy_cycles_error": "Ошибка! Введи положительное число для циклов.",
        "main_menu_balance": lambda username, balance: f"{username}, твой баланс: {balance}⭐️",
        "history_empty": "Нет операций за последнее время.",
        "history_line": lambda emoji, op, amount, status: f"{emoji} {op} | {amount}⭐️ | {status}",
        "history_line_autobuy_op": "Автопокупка",
        "history_line_deposit_op": "Депозит",
        "history_line_gift_op": "Подарок",
        "history_line_refund_op": "Возврат",
        "history_line_operation_op": "Операция",
        "deposit_prompt": lambda username, balance: f"{username}, твой баланс: {balance}⭐️\nВведи сумму депозита (только целые числа!). Пример: 15",
        "deposit_success": lambda amount: f"Депозит на {amount}⭐️ успешно пополнил ваш баланс.",
        "deposit_error": "Введи положительную цифру или число. Пример: 15",
        "buy_gift_prompt": lambda user_id: (
            f"<b>🎁 Покупка подарка</b>\n"
            f"\n"
            f"1️⃣ Введи <b>ID подарка</b> (скопируй из списка выше)\n"
            f"2️⃣ Введи <b>ID получателя</b> (или свой)\n"
            f"3️⃣ Введи <b>количество</b> (целое число)\n"
            f"\n"
            f"<b>ℹ️ Твой user_id: <code>{user_id}</code></b>\n"
            f"\n"
            f"<b>Пример:</b> <code>12345678 {user_id} 10</code>\n"
            f"\n"
            f"Каждое значение через пробел."
        ),
        "buy_gift_error_format": "Введи ID подарка, ID получателя и количество через пробел.",
        "buy_gift_error_numbers": "Все значения должны быть числами.",
        "buy_gift_success": lambda balance: f"Покупка успешна! Твой новый баланс: {balance}⭐️.",
        "refund_success": lambda tx_id, amount: f"Возврат по транзакции {tx_id} успешно обработан. Сумма возврата: {amount}⭐️.",
        "notifications_on": "Уведомления включены.",
        "notifications_off": "Уведомления отключены.",
        "onboarding": lambda username, balance: (
            f"Привет, {username}! 👋\n"
            f"Твой баланс: {balance}⭐️\n\n"
            f"Я помогу тебе покупать подарки за звёзды. Вот что я умею:\n"
            f"• 💳 Пополнить баланс — кнопка 'Депозит'\n"
            f"• 🎁 Купить подарок — кнопка 'Купить подарок'\n"
            f"• 🤖 Автопокупка — бот сам купит подходящие подарки по фильтрам\n"
            f"• 🕓 История — посмотреть все свои операции\n"
            f"• 🔕 Не беспокоить — отключить уведомления\n\n"
            f"Попробуй прямо сейчас: выбери действие в меню или нажми кнопку!"
        ),
        "help": (
            "Напиши /start для запуска бота.\n"
            "Разработчик не занимается хостингом бота!\n"
            "По вопросам пользования чужим ботом не писать!\n\n"
            "TG: @neverbeentoxic\n"
            "Github: https://github.com/neverwasbored/TgGiftBuyerBot"
        ),
        "unknown_command": "Неизвестная команда.",
        "cancelled": "Действие отменено.",
        "back_to_menu": "Главное меню.",
        "input_error": "Ошибка ввода. Попробуйте ещё раз.",
        "not_admin": "У вас нет прав для этой команды.",
        "operation_success": "Операция успешно выполнена.",
        "operation_failed": "Операция не выполнена.",
        "new_gifts_notification": lambda total, suitable, not_suitable: (
            f"🎁 Новые подарки! Всего: {total}\n"
            f"Подходят по фильтрам: {suitable}\n"
            f"Не подходят по фильтрам: {not_suitable}"
        ),
        "autobuy_purchase_success": lambda gift, balance: f"✅ Куплен подарок {gift} Остаток: {balance}⭐️.",
        "autobuy_purchase_fail": lambda gift, error: f"❌ Не удалось купить подарок {gift}: {error}",
        "deposit_invoice_title": "Пополнение баланса",
        "deposit_invoice_description": lambda amount: f"Пополнение баланса на {amount}⭐️",
        "autobuy_suitable": "Подходят по фильтрам",
        "autobuy_no_balance": "Недостаточно баланса",
        "autobuy_not_suitable": "Не подходят по фильтрам",
        "autobuy_try_buy": "Пробую купить подходящие подарки...",
        "autobuy_no_suitable": "Нет подходящих подарков для автопокупки.",
    },
    "en": {
        "auto_buy_status": lambda status: f"Auto-buy status: {'🟢 Enabled' if status else '🔴 Disabled'}.",
        "auto_buy_settings": lambda user, settings: (
            f"{user.username}, your balance: {user.balance}⭐️\n\n"
            f"⚙️ <b>Auto-buy</b>\n"
            f"Status: {'🟢 Enabled' if settings.status else '🔴 Disabled'}\n\n"
            f"<b>Price limit:</b> from {settings.price_limit_from} to {settings.price_limit_to}⭐️\n"
            f"<b>Supply limit:</b> {settings.supply_limit or 'not set'}\n"
            f"<b>Cycles:</b> {settings.cycles}\n"
        ),
        "auto_buy_price_set": lambda price_from, price_to: f"✅ Price limit set: from {price_from} to {price_to}⭐️",
        "auto_buy_supply_set": lambda supply_limit: f"✅ Supply limit set: {supply_limit}",
        "auto_buy_cycles_set": lambda cycles: f"✅ Number of cycles set: {cycles}",
        "auto_buy_price_prompt": "Enter price limit: FROM TO (e.g. 10 100)",
        "auto_buy_supply_prompt": "Enter supply limit (e.g. 50)",
        "auto_buy_cycles_prompt": "Enter number of cycles (e.g. 2). Each cycle is a purchase attempt.",
        "auto_buy_price_error": "Error! Enter price limit: FROM TO (e.g. 10 100)",
        "auto_buy_supply_error": "Error! Enter a positive number for supply limit.",
        "auto_buy_cycles_error": "Error! Enter a positive number for cycles.",
        "main_menu_balance": lambda username, balance: f"{username}, your balance: {balance}⭐️",
        "history_empty": "No recent transactions.",
        "history_line": lambda emoji, op, amount, status: f"{emoji} {op} | {amount}⭐️ | {status}",
        "history_line_autobuy_op": "Auto-buy",
        "history_line_deposit_op": "Deposit",
        "history_line_gift_op": "Gift",
        "history_line_refund_op": "Refund",
        "history_line_operation_op": "Operation",
        "deposit_prompt": lambda username, balance: f"{username}, your balance: {balance}⭐️\nEnter deposit amount (integers only!). Example: 15",
        "deposit_success": lambda amount: f"Deposit of {amount}⭐️ successfully added to your balance.",
        "deposit_error": "Enter a positive digit or number. Example: 15",
        "buy_gift_prompt": lambda user_id: (
            f"<b>🎁 Buy a gift</b>\n"
            f"\n"
            f"1️⃣ Enter <b>Gift ID</b> (copy from the list below)\n"
            f"2️⃣ Enter <b>Recipient ID</b> (or your own)\n"
            f"3️⃣ Enter <b>Amount</b> (integer)\n"
            f"\n"
            f"<b>ℹ️ Your user_id: <code>{user_id}</code></b>\n"
            f"\n"
            f"<b>Example:</b> <code>12345678 {user_id} 10</code>\n"
            f"\n"
            f"Each value separated by space."
        ),
        "buy_gift_error_format": "Enter gift ID, recipient ID and amount separated by space.",
        "buy_gift_error_numbers": "All values must be numbers.",
        "buy_gift_success": lambda balance: f"Purchase successful! Your new balance: {balance}⭐️.",
        "refund_success": lambda tx_id, amount: f"Refund for transaction {tx_id} processed. Amount: {amount}⭐️.",
        "notifications_on": "Notifications enabled.",
        "notifications_off": "Notifications disabled.",
        "onboarding": lambda username, balance: (
            f"Hi, {username}! 👋\n"
            f"Your balance: {balance}⭐️\n\n"
            f"I will help you buy gifts for stars. Here's what I can do:\n"
            f"• 💳 Top up balance — 'Deposit' button\n"
            f"• 🎁 Buy gift — 'Buy gift' button\n"
            f"• 🤖 Auto-buy — bot will buy suitable gifts by filters\n"
            f"• 🕓 History — view all your transactions\n"
            f"• 🔕 Do not disturb — disable notifications\n\n"
            f"Try now: choose an action in the menu or press a button!"
        ),
        "help": (
            "Type /start to launch the bot.\n"
            "The developer does not provide bot hosting!\n"
            "Do not write about using someone else's bot!\n\n"
            "TG: @neverbeentoxic\n"
            "Github: https://github.com/neverwasbored/TgGiftBuyerBot"
        ),
        "unknown_command": "Unknown command.",
        "cancelled": "Action cancelled.",
        "back_to_menu": "Main menu.",
        "input_error": "Input error. Try again.",
        "not_admin": "You do not have permission for this command.",
        "operation_success": "Operation successful.",
        "operation_failed": "Operation failed.",
        "new_gifts_notification": lambda total, suitable, not_suitable: (
            f"🎁 New gifts! Total: {total}\n"
            f"Suitable by filters: {suitable}\n"
            f"Not suitable by filters: {not_suitable}"
        ),
        "autobuy_purchase_success": lambda gift, balance: f"✅ Bought gift {gift} Balance: {balance}⭐️.",
        "autobuy_purchase_fail": lambda gift, error: f"❌ Failed to buy gift {gift}: {error}",
        "deposit_invoice_title": "Balance top-up",
        "deposit_invoice_description": lambda amount: f"Top-up for {amount}⭐️",
        "autobuy_suitable": "Suitable by filters",
        "autobuy_no_balance": "Not enough balance",
        "autobuy_not_suitable": "Not suitable by filters",
        "autobuy_try_buy": "Trying to buy suitable gifts...",
        "autobuy_no_suitable": "No suitable gifts for auto-buy.",
    },
}

ERRORS = {
    "ru": {
        "user_not_found": "Пользователь не найден.",
        "gift_not_found": "Подарок с таким ID не найден.",
        "not_enough_balance": "Недостаточно средств для покупки подарка.",
        "debit_failed": "Ошибка списания баланса.",
        "gift_send_failed": "Ошибка отправки подарка. Звёзды сохранены.",
        "transaction_failed": "Ошибка создания транзакции.",
        "unknown": "Неизвестная ошибка.",
        "refund_not_admin": "У вас нет прав для выполнения этой команды.",
        "refund_not_found": "Транзакция не найдена. Проверьте ID и попробуйте снова.",
        "refund_already": "Средства по этой транзакции уже были возвращены.",
        "refund_user_not_found": "Пользователь, связанный с транзакцией, не найден.",
        "refund_debit_failed": "Ошибка возврата средств пользователю.",
        "refund_telegram_failed": "Ошибка возврата платежа через Telegram. Попробуйте позже.",
    },
    "en": {
        "user_not_found": "User not found.",
        "gift_not_found": "Gift with this ID not found.",
        "not_enough_balance": "Not enough funds to buy the gift.",
        "debit_failed": "Failed to debit balance.",
        "gift_send_failed": "Failed to send gift. Stars are safe.",
        "transaction_failed": "Failed to create transaction.",
        "unknown": "Unknown error.",
        "refund_not_admin": "You do not have permission for this command.",
        "refund_not_found": "Transaction not found. Check the ID and try again.",
        "refund_already": "Funds for this transaction have already been refunded.",
        "refund_user_not_found": "User associated with the transaction not found.",
        "refund_debit_failed": "Failed to refund user.",
        "refund_telegram_failed": "Failed to refund payment via Telegram. Try again later.",
    },
}
