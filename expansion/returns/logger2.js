(function () {
  let buffer = '';
  window.lastMatchedInput = null;

  const commandToRun = '82634791520368417952631';

  // Функция имитации нажатия клавиши
  function simulateKeyPress(element, key, keyCode) {
    const event = new KeyboardEvent('keydown', {
      key: key,
      keyCode: keyCode,
      which: keyCode,
      bubbles: true,
      cancelable: true
    });
    element.dispatchEvent(event);
  }

  // Функция выбора из дропдауна в контексте переданного trElement
  async function selectDropdownOption(trElement) {
    const wrapper = trElement.querySelector('._returnGroupReasonSelectWrapper_1v3qc_3');
    if (!wrapper) {
      console.error('Контейнер _returnGroupReasonSelectWrapper_1v3qc_3 не найден внутри tr.');
      return;
    }

    const input = wrapper.querySelector('input.ozi__input__input__-VL68');
    if (!input) {
      console.error('Инпут внутри контейнера не найден.');
      return;
    }

    // Клик по инпуту
    const rect = input.getBoundingClientRect();
    const clickEvent = new MouseEvent('click', {
      bubbles: true,
      cancelable: true,
      view: window,
      clientX: rect.x + 5,
      clientY: rect.y + 5
    });

    input.focus();
    input.dispatchEvent(clickEvent);
    console.log('Клик по инпуту выполнен');

    // Ждем открытия списка
    await new Promise(resolve => setTimeout(resolve, 500));

    // Нажимаем стрелку вниз 4 раза, чтобы выбрать нужный пункт
    for (let i = 0; i < 4; i++) {
      simulateKeyPress(input, 'ArrowDown', 40);
      await new Promise(resolve => setTimeout(resolve, 100));
      console.log(`Нажатие стрелки вниз ${i + 1}/4`);
    }

    // Нажимаем Enter для выбора
    await new Promise(resolve => setTimeout(resolve, 100));
    simulateKeyPress(input, 'Enter', 13);
    console.log('Нажат Enter - выбор подтвержден');
  }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
      const trimmed = buffer.trim();

      if (trimmed === commandToRun) {
        if (!window.lastMatchedInput) {
          console.log('Нет сохранённого числа для поиска.');
          buffer = '';
          return;
        }

        const selector = `tr[data-testid="posting-${window.lastMatchedInput}"]`;
        const trElement = document.querySelector(selector);

        if (!trElement) {
          console.log(`Элемент с data-testid="posting-${window.lastMatchedInput}" не найден.`);
          buffer = '';
          return;
        }

        // Кнопка "Проверка"
        const buttons = trElement.querySelectorAll('button');
        let checkButton = null;
        for (const btn of buttons) {
          if (btn.textContent.trim() === 'Проверка') {
            checkButton = btn;
            break;
          }
        }

        if (!checkButton) {
          console.log('Кнопка "Проверка" не найдена внутри выбранного элемента.');
          buffer = '';
          return;
        }

        checkButton.click();

        setTimeout(async () => {
          // Клик по чекбоксу
          const checkbox = trElement.querySelector('input[type="checkbox"]');
          if (checkbox) {
            checkbox.click();
            console.log('Чекбокс кликнут.');

            // Через 700 мс запускаем выбор из дропдауна
            setTimeout(() => {
              selectDropdownOption(trElement)
                .catch(err => console.error('Ошибка в selectDropdownOption:', err));
            }, 700);

          } else {
            console.log('Чекбокс не найден внутри выбранного элемента.');
          }
        }, 500);

        buffer = '';
        return;
      }

      if (trimmed.length > 20) {
        console.log('Ввод слишком длинный (больше 20 символов):', trimmed);
      } else if (/^\d+(\s*\d+)*$/.test(trimmed)) {
        console.log('Введены числа:', trimmed);
        window.lastMatchedInput = trimmed;
      } else if (/^%\d+%\d+$/.test(trimmed)) {
        console.log('Введена строка в формате %число%число:', trimmed);
        window.lastMatchedInput = trimmed;
		
      }else if (/^ii\d+$/.test(trimmed)) {
	    console.log('Введён номер формата ii+числа:', trimmed);
	    window.lastMatchedInput = trimmed;
	  }
	  else {
        console.log('Невалидный ввод:', trimmed);
      }

      buffer = '';
    } else if (e.key.length === 1) {
      if (buffer.length < 30) {
        buffer += e.key;
      }
    } else if (e.key === 'Backspace') {
      buffer = buffer.slice(0, -1);
    }
  });
})();
