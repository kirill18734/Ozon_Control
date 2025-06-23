const previousCodes = new Set();

function isValidCode(code) {
    return /^\d{1,}-\d+$/.test(code); // Пример: 422-4352
}

function sendToServer(text) {
    fetch("http://127.0.0.1:4025/print", {
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

        // если этот код не был ранее зафиксирован
        if (!previousCodes.has(code)) {
            previousCodes.add(code);
            console.log("📦 Новый номер:", code);
            sendToServer(code);
        }
    }
}

// Запуск наблюдателя, чтобы вызывать `scanAndCompare` при изменениях DOM
const observer = new MutationObserver(() => {
    scanAndCompare();
});

function start() {
    const targetNode = document.querySelector('._logsWrapper_1igxv_7');
    if (targetNode) {
        observer.observe(targetNode, { childList: true, subtree: true });
        console.log("✅ Запущено наблюдение за DOM");
        scanAndCompare(); // сразу сканируем текущие элементы
    } else {
        console.warn("❌ Контейнер не найден, повтор через 1 сек...");
        setTimeout(start, 1000);
    }
}

start();
