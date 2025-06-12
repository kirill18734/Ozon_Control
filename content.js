const scannedMap = new Map(); // вместо Set, чтобы хранить время последней отправки
const RESEND_INTERVAL_MS = 3000; // повторная отправка через 3 секунды

function sendToServer(text) {
    fetch("http://127.0.0.1:4025/print", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text })
    }).then(res => res.json())
      .then(data => console.log("📤 Отправлено на сервер:", data))
      .catch(err => console.error("❌ Ошибка:", err));
}

const observer = new MutationObserver((mutationsList) => {
    const now = Date.now();

    for (const mutation of mutationsList) {
        const newItems = mutation.target.querySelectorAll('[data-testid="logItemPlace"]');
        for (const item of newItems) {
            const code = item.textContent.trim();

            const lastSent = scannedMap.get(code);
            if (!lastSent || (now - lastSent > RESEND_INTERVAL_MS)) {
                scannedMap.set(code, now);
                console.log(lastSent ? "🔁 Повторно отправлено:" : "📦 Новый номер:", code);
				
                sendToServer(code);
            }
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
