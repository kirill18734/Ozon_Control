const previousCodes = new Set();
const href_reciepts_goods = "https://turbo-pvz.ozon.ru/receiving/receive";
const local_url_send_to_server = "http://127.0.0.1:4025/print";
const timeout_sec = 1000;

let currentHref = location.href;
let observer = null;

function isValidCode(code) {
    return /^\d{1,}-\d+$/.test(code);
}

function sendToServer(text) {
    fetch(local_url_send_to_server, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text })
    })
    .then(res => res.json())
    .then(data => console.log("📤 Отправлено на сервер:", data))
    .catch(err => console.error("❌ Ошибка:", err));
}

function scanAndCompare() {
    const items = document.querySelectorAll('[data-testid="logItemPlace"]');
    const currentCodes = new Set();

    for (const item of items) {
        const code = item.textContent.trim();
        if (!isValidCode(code)) {
            console.warn("⛔ Некорректный формат:", code);
            continue;
        }

        currentCodes.add(code);

        if (!previousCodes.has(code)) {
            previousCodes.add(code);
            console.log("📦 Новый номер:", code);
            sendToServer(code);
        }
    }
}

function observeIfOnCorrectPage() {
    if (location.href === href_reciepts_goods) {
        console.log(`✅ Перешли на нужную страницу: ${href_reciepts_goods}`);

        const targetNode = document.querySelector('._logsWrapper_1igxv_7');

        if (targetNode) {
            if (observer) observer.disconnect(); // Отключаем предыдущий наблюдатель, если был
            observer = new MutationObserver(scanAndCompare);
            observer.observe(targetNode, {
                childList: true,
                subtree: true
            });
            console.log(`🔍 Наблюдение за DOM начато`);
            scanAndCompare();
        } else {
            console.warn(`❌ Элемент для наблюдения не найден`);
        }
    } else {
        if (observer) {
            observer.disconnect();
            observer = null;
            console.log("🛑 Вышли с нужной страницы, наблюдение остановлено");
        }
    }
}

// Проверяем смену URL
setInterval(() => {
    if (location.href !== currentHref) {
        currentHref = location.href;
        previousCodes.clear(); // очищаем прошлые коды при смене страницы
        console.log("🔄 URL изменился:", currentHref);
        observeIfOnCorrectPage();
    }
}, timeout_sec); // Проверка URL раз в секунду — это нормально, потому что без лишней логики

// Первая инициализация
observeIfOnCorrectPage();
