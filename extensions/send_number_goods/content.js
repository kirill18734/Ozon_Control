const previousCodes = new Set();
const href_reciepts_goods = "https://turbo-pvz.ozon.ru/receiving/receive";
const local_url_send_to_server = "http://127.0.0.1:4025/print";
const find_selector = "._logsWrapper_1igxv_7"
const timeout_sec = 1000;

function isValidCode(code) {
    return /^\d{1,}-\d+$/.test(code); // Пример: 422-4352
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
    const targetNode = document.querySelector(find_selector);
    if (location.href == href_reciepts_goods){
        console.log("✅ Вы вошли на нужный сайт");
    if (targetNode) {
        observer.observe(targetNode, { childList: true, subtree: true });
        console.log(`✅Удалось найти нужный элемент: ${find_selector}. Скрипт на мониторинг номеров запущен`);
        scanAndCompare(); // сразу сканируем текущие элементы
    } else {
        console.warn(`❌ Не удалось найти элемент ${find_selector}.`);
        setTimeout(start, timeout_sec);
    }}
    else {
     console.warn(`❌ Вы не находитесь на нужном сайте: ${href_reciepts_goods} `);
     setTimeout(start, timeout_sec);
    }
}

start();