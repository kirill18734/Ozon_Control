let buffer = "";
let isRunning = false;

// Универсальная функция ожидания и клика
function waitAndClick(target, timeout = 3000) {
    return new Promise((resolve, reject) => {
        const startTime = Date.now();

        function tryClick() {
            let btn = null;

            if (target.startsWith("text:")) {
                const text = target.slice(5).trim().toLowerCase();
                btn = [...document.querySelectorAll("button, [role='button']")].find(el =>
                    el.textContent.trim().toLowerCase().includes(text)
                );
            } else {
                btn = document.querySelector(target);
            }

            if (btn) {
                btn.click();
                console.log(`Нажата кнопка: ${target}`);
                resolve(true);
            } else if (Date.now() - startTime >= timeout) {
                console.warn(`Кнопка не найдена за ${timeout} мс: ${target}`);
                reject(false);
            } else {
                requestAnimationFrame(tryClick);
            }
        }

        tryClick();
    });
}

// Проверка существования элемента по тексту
function elementWithTextExists(text) {
    const lowerText = text.toLowerCase();
    return [...document.querySelectorAll("button, [role='button']")].some(el =>
        el.textContent.toLowerCase().includes(lowerText)
    );
}

// Обработка комбинации
async function handleCombination(matchText, actions, actionName) {
    if (!buffer.includes(matchText)) return;

    console.log(`Комбинация найдена: ${actionName}`);
    buffer = "";

    for (const action of actions) {
        try {
            await waitAndClick(action);
            await new Promise(r => setTimeout(r, 500));
        } catch {
            console.log(`Прекращаем выполнение оставшихся кликов (${actionName})`);
            break;
        }
    }
}

// Универсальный цикл "К выдаче"
async function startToIssueLoopGeneric(actions) {
    if (isRunning) return;
    isRunning = true;

    console.log("Запуск цикла обработки 'К выдаче'");
    try {
        while (elementWithTextExists("К выдаче")) {
            await waitAndClick("text:К выдаче");
            await new Promise(r => setTimeout(r, 500));

            for (const action of actions) {
                await waitAndClick(action);
                await new Promise(r => setTimeout(r, 500));
            }
        }
    } catch (err) {
        console.warn("Ошибка в процессе цикла");
    }

    console.log("Цикл 'К выдаче' завершён");
    isRunning = false;
}

// Обработка ввода
document.addEventListener("keydown", async function (e) {
    if (e.key.length === 1) {
        buffer += e.key;
        if (buffer.length > 50) buffer = buffer.slice(-50);

        await handleCombination(
            "37821563489167429583100",
            [
                "text:Продолжить",
                "text:Не выдавать пакеты",
                "text:Выдать",
                "text:На главную"
            ],
            "Выдать заказ (без пакета)"
        );

        await handleCombination(
            "60418273951624830975261",
            [
                "text:Продолжить",
                'button[class*="increment"]',
                "text:Выдать 1 пакет",
                "text:Выдать",
                "text:На главную"
            ],
            "Выдать заказ (+1 пакет)"
        );

        await handleCombination(
            "920374615208431975286391",
            [
                'input.ozi__toggle__toggle__2ImSG'
            ],
            "Автораспределение"
        );

        if (buffer.includes("91347265019832476015342")) {
            buffer = "";
            await startToIssueLoopGeneric([
                "text:Продолжить",
                'button[class*="increment"]',
                "text:Выдать 1 пакет",
                "text:Выдать",
                "text:На главную"
            ]);
        }

        if (buffer.includes("74892015376184239061527")) {
            buffer = "";
            await startToIssueLoopGeneric([
                "text:Продолжить",
                "text:Не выдавать пакеты",
                "text:Выдать",
                "text:На главную"
            ]);
        }
		if (buffer.includes("70983625147892016354712")) {
            buffer = "";
            await startToIssueLoopGeneric([
                "text:Продолжить",
                "text:Не выдавать пакеты",
                "text:Оплатить"
            ]);
        }
    }
});
