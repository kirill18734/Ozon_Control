(function () {
  let buffer = '';
  window.lastMatchedInput = null;

  const commandToRun = '82634791520368417952631';

  // Перевод русских букв в английскую раскладку (только буквы)
  function convertCyrillicToLatin(input) {
    const layout = {
      'а': 'f', 'б': ',', 'в': 'd', 'г': 'u', 'д': 'l',
      'е': 't', 'ё': '`', 'ж': ';', 'з': 'p', 'и': 'b',
      'й': 'q', 'к': 'r', 'л': 'k', 'м': 'v', 'н': 'y',
      'о': 'j', 'п': 'g', 'р': 'h', 'с': 'c', 'т': 'n',
      'у': 'e', 'ф': 'a', 'х': '[', 'ц': 'w', 'ч': 'x',
      'ш': 'i', 'щ': 'o', 'ъ': ']', 'ы': 's', 'ь': 'm',
      'э': '\'', 'ю': '.', 'я': 'z',
    };

    return input.replace(/[а-яё]/gi, char => {
      const lower = char.toLowerCase();
      const isUpper = char !== lower;
      const latin = layout[lower] || char;
      return isUpper ? latin.toUpperCase() : latin;
    });
  }

  // Имитация нажатия клавиши
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

  // Выбор пункта в выпадающем списке
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

    await new Promise(resolve => setTimeout(resolve, 500));

    for (let i = 0; i < 4; i++) {
      simulateKeyPress(input, 'ArrowDown', 40);
      await new Promise(resolve => setTimeout(resolve, 100));
      console.log(`Нажатие стрелки вниз ${i + 1}/4`);
    }

    await new Promise(resolve => setTimeout(resolve, 100));
    simulateKeyPress(input, 'Enter', 13);
    console.log('Нажат Enter - выбор подтвержден');
  }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
      const trimmed = buffer.trim();
      const converted = convertCyrillicToLatin(trimmed);
      console.log(`Преобразовано: "${trimmed}" → "${converted}"`);

      if (converted === commandToRun) {
        if (!window.lastMatchedInput) {
          console.log('Нет сохранённого числа для поиска.');
          buffer = '';
          return;
        }

        // Поиск tr по текстовому содержимому
        const allTrs = document.querySelectorAll('tr[data-testid^="posting-"]');
        let trElement = null;

        for (const tr of allTrs) {
          if (tr.textContent.includes(window.lastMatchedInput)) {
            trElement = tr;
            break;
          }
        }

        if (!trElement) {
          console.log(`Не найден tr, содержащий номер: ${window.lastMatchedInput}`);
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
          const checkbox = trElement.querySelector('input[type="checkbox"]');
          if (checkbox) {
            checkbox.click();
            console.log('Чекбокс кликнут.');

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

      // Сохранение последнего найденного значения
      if (converted.length > 20) {
        console.log('Ввод слишком длинный (больше 20 символов):', converted);
      } else if (/^\d+(\s*\d+)*$/.test(converted)) {
        console.log('Введены числа:', converted);
        window.lastMatchedInput = converted;
      } else if (/^%\d+%\d+$/.test(converted)) {
        console.log('Введена строка в формате %число%число:', converted);
        window.lastMatchedInput = converted;
      } else if (/^ii\d+$/.test(converted)) {
        console.log('Введён номер формата ii+числа:', converted);
        window.lastMatchedInput = converted;
      } else {
        console.log('Невалидный ввод:', converted);
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
