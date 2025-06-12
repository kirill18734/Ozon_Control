const scannedSet = new Set(); // сохраняем только уникальные значения

function isValidCode(code) {
    return /^\d{3,}-\d+$/.test(code); // Пример: 422-4352
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

const observer = new MutationObserver((mutationsList) => {
    for (const mutation of mutationsList) {
        const newItems = mutation.target.querySelectorAll('[data-testid="logItemPlace"]');
        for (const item of newItems) {
            const code = item.textContent.trim();

            if (!isValidCode(code)) {
                console.warn("⛔ Некорректный формат:", code);
                continue;
            }

            if (scannedSet.has(code)) {
                console.log("🔁 Уже отправлено ранее:", code);
                continue;
            }

            scannedSet.add(code);
            console.log("📦 Новый номер:", code);
            sendToServer(code);
        }
    }
});

function start() {
    const targetNode = document.querySelector('._logsWrapper_1igxv_7');
    if (targetNode) {
        observer.observe(targetNode, { childList: true, subtree: true });
        console.log("✅ Запущено наблюдение за DOM");
    } else {
        console.warn("❌ Контейнер не найден, повтор через 1 сек...");
        setTimeout(start, 1000);
    }
}

start();
