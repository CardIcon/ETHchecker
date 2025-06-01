# ETHchecker

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge"/>
  <img src="https://img.shields.io/badge/Etherscan-213259?style=for-the-badge&logo=etherscan&logoColor=white" alt="Etherscan Badge"/>
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License Badge"/>
  <h1>🚀 Ethereum Random Wallet Explorer & Balance Checker</h1>
  <p>
    Python-скрипт для генерации случайных Ethereum адресов и проверки их баланса через Etherscan API.
    Создан для демонстрации работы с криптографической генерацией ключей, внешними API и автоматизацией.
  </p>
</div>

---

<h2>⚠️ Важное Этическое Примечание / Disclaimer</h2>
<p>
  Этот инструмент разработан и предназначен <strong>исключительно для образовательных, исследовательских и демонстрационных целей</strong>.
  Он позволяет понять, как случайные приватные ключи генерируются и как их можно связать с публичными адресами и проверять их статус через блокчейн API.
</p>
<p>
  <strong>Категорически не рекомендуется и осуждается использование этого скрипта для любых незаконных, неэтичных или вредоносных действий, включая попытки несанкционированного доступа к чужим средствам.</strong>
  Практически невозможно "угадать" или "брутфорснуть" приватный ключ существующего Ethereum кошелька из-за астрономического количества возможных комбинаций (2^256).
  Любые попытки использования данного кода для этих целей будут неэффективными и могут иметь юридические последствия.
</p>
<p>
  Разработчик и автор этого репозитория не несут ответственности за любое неправомерное использование данного программного обеспечения.
</p>

---

<h2>✨ Возможности</h2>
<ul>
  <li>Генерация случайных и криптографически надежных приватных ключей и Ethereum адресов.</li>
  <li>Проверка текущего ETH баланса сгенерированных адресов через официальный Etherscan API.</li>
  <li>Автоматическая запись найденных кошельков с ненулевым балансом в локальный файл.</li>
  <li>Управление скоростью запросов для соответствия лимитам Etherscan API.</li>
  <li>Яркий и информативный вывод в консоль.</li>
  <li>Безопасное хранение API ключа через переменные окружения.</li>
</ul>

---

<h2>🛠 Технологии</h2>
<ul>
  <li><img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"> <strong>Python 3.x</strong></li>
  <li><img src="https://img.shields.io/badge/Requests-26216A?style=flat-square&logo=python&logoColor=white" alt="Requests"> <strong>Requests</strong> (для HTTP запросов к API)</li>
  <li><img src="https://img.shields.io/badge/Eth--Account-000000?style=flat-square&logo=ethereum&logoColor=white" alt="Eth-Account"> <strong>Eth-Account</strong> (для генерации Ethereum ключей)</li>
  <li><img src="https://img.shields.io/badge/Etherscan%20API-213259?style=flat-square&logo=etherscan&logoColor=white" alt="Etherscan API"> <strong>Etherscan API</strong> (для получения данных о балансах)</li>
</ul>

---

<h2>🚀 Быстрый Старт</h2>

<h3>Предварительные требования</h3>
<p>Для запуска скрипта вам понадобится:</p>
<ul>
  <li>Python 3.x.</li>
  <li>Бесплатный API ключ Etherscan. Вы можете получить его здесь: <a href="https://etherscan.io/myaccount">Etherscan MyAccount</a>.</li>
</ul>

<h3>Установка зависимостей</h3>
<p>Установите необходимые Python библиотеки:</p>
<pre><code>pip install requests eth-account
</code></pre>

<h3>Настройка API ключа Etherscan</h3>
<p><strong>Не вставляйте API ключ непосредственно в код!</strong> Для безопасности и удобства используйте переменные окружения. Перезагрузите терминал/командную строку после установки переменной.</p>
<p><strong>Для Linux/macOS (Terminal):</strong></p>
<pre><code>export ETHERSCAN_API_KEY="ВАШ_КЛЮЧ_ОТ_ETHERSCAN"
</code></pre>
<p><strong>Для Windows (Command Prompt):</strong></p>
<pre><code>set ETHERSCAN_API_KEY="ВАШ_КЛЮЧ_ОТ_ETHERSCAN"
</code></pre>
<p><strong>Для Windows (PowerShell):</strong></p>
<pre><code>$env:ETHERSCAN_API_KEY="ВАШ_КЛЮЧ_ОТ_ETHERSCAN"
</code></pre>
<p>Замените <code>ВАШ_КЛЮЧ_ОТ_ETHERSCAN</code> на ваш реальный ключ.</p>

<h3>Запуск скрипта</h3>
<p>После установки зависимостей и настройки API ключа, вы можете запустить скрипт:</p>
<pre><code>python eth_wallet_scanner.py
</code></pre>
<p>Нажмите <code>Ctrl+C</code> в любой момент, чтобы остановить выполнение программы.</p>

---

<h2>⚙️ Конфигурация (внутри <code>eth_wallet_scanner.py</code>)</h2>
<p>Вы можете настроить следующие параметры, изменив их непосредственно в файле <code>eth_wallet_scanner.py</code>:</p>
<ul>
  <li><code>OUTPUT_FILE</code>: Имя файла для сохранения найденных кошельков.</li>
  <li><code>REQUEST_DELAY</code>: Задержка в секундах между запросами к API.</li>
  <li><code>DAILY_CALL_LIMIT</code>: Предполагаемый дневной лимит запросов к Etherscan API.</li>
</ul>

---

<h2>📜 Лицензия</h2>
<p>
  Данный проект распространяется под лицензией MIT. Подробности см. в файле <a href="LICENSE">LICENSE</a>.
</p>

---

<h2>🤝 Авторство и Поддержка</h2>
<ul>
  <li><strong>Оригинальный Автор:</strong> XZLKT</li>
  <li><strong>Представлено и Поддерживается:</strong> <a href="https://github.com/CardIcon">@CardIcon</a></li>
</ul>
<p>
  Если у вас есть вопросы или предложения, не стесняйтесь связаться со мной через мой основной профиль GitHub.
</p>
