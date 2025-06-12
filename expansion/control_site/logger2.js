let buffer = "";

// Универсальная функция ожидания и клика по селектору или тексту
function waitAndClick(target, timeout = 3000) {
    return new Promise((resolve, reject) => {
        const startTime = Date.now();

        function tryClick() {
            let btn = null;

            if (target.startsWith("text:")) {
                const text = target.slice(5).trim().toLowerCase();
                btn = [...document.querySelectorAll("button, [role='button']")].find(el =>
                    el.textContent.trim().toLowerCase() === text
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

// Проверка, существует ли элемент с текстом
function elementWithTextExists(text) {
    const lowerText = text.toLowerCase();
    return [...document.querySelectorAll("button, [role='button']")].some(el =>
        el.textContent.trim().toLowerCase() === lowerText
    );
}

// Основная обработка комбинации
function handleCombination(matchText, actions, actionName) {
    if (!buffer.includes(matchText)) return;

    console.log(`Комбинация найдена: ${actionName}`);
    buffer = ""; // сбрасываем сразу

    (async () => {
        for (let i = 0; i < actions.length; i++) {
            try {
                await waitAndClick(actions[i]);
                await new Promise(r => setTimeout(r, 500)); // Задержка между кликами
            } catch {
                console.log(`Прекращаем выполнение оставшихся кликов (${actionName})`);
                break;
            }
        }
    })();
}

// Обработка цикла для "К выдаче"
async function startToIssueLoop() {
    console.log("Запуск цикла обработки 'К выдаче'");
    while (elementWithTextExists("К выдаче")) {
        try {
            await waitAndClick("text:К выдаче");
            await new Promise(r => setTimeout(r, 500));

            const actions = [
                "text:Продолжить",
                "text:Не выдавать пакеты",
                "text:Выдать",
                "text:На главную"
            ];

            for (let i = 0; i < actions.length; i++) {
                await waitAndClick(actions[i]);
                await new Promise(r => setTimeout(r, 500));
            }
        } catch (err) {
            console.warn("Ошибка в процессе или кнопка исчезла");
            break;
        }
    }
    console.log("Цикл 'К выдаче' завершён – кнопка больше не найдена");
}

// Слушаем ввод
document.addEventListener("keydown", function (e) {
    if (e.key.length === 1) {
        buffer += e.key;
        if (buffer.length > 50) buffer = buffer.slice(-50);

        handleCombination(
            "37821563489167429583100",
            [
                "text:Продолжить",
                "text:Не выдавать пакеты",
                "text:Выдать",
                "text:На главную"
            ],
            "Выдать заказ (без пакета)"
        );

        handleCombination(
            "60418273951624830975261",
            [
                "text:Продолжить",
                'button.ozi__input-count__increment__eQ8gA',
                "text:Выдать 1 пакет",
                "text:Выдать",
                "text:На главную"
            ],
            "Выдать заказ (+1 пакет)"
        );

        handleCombination(
            "920374615208431975286391",
            [
                'input.ozi__toggle__toggle__1Wno_'
            ],
            "Автораспределение"
        );

        // Комбинация для старта цикла "К выдаче"
        if (buffer.includes("91347265019832476015342")) {
            buffer = "";
            startToIssueLoop();
        }
    }
});
