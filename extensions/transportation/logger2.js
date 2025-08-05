(function () {
  const keywords = ["Угги", "ii9082036526", "Возврат-2"]; // все слова должны присутствовать
  const classPrefix = "_element";

  function containsAllKeywords(text) {
    return keywords.every(keyword => text.includes(keyword));
  }

  function removeTargetDivs() {
    document.querySelectorAll(`div[class^="${classPrefix}"]`).forEach(div => {
      const text = div.textContent;
      if (containsAllKeywords(text)) {
        div.remove();
        console.log("Удалён элемент, содержащий все ключевые слова:", div);
      }
    });
  }

  // Наблюдение за изменениями в DOM
  const observer = new MutationObserver(() => {
    removeTargetDivs();
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true,
  });

  // Отслеживание изменений URL
  let lastUrl = location.href;
  setInterval(() => {
    if (location.href !== lastUrl) {
      lastUrl = location.href;
      console.log("URL изменился, перезапуск удаления...");
      removeTargetDivs();
    }
  }, 1000);

  // Первоначальный запуск
  removeTargetDivs();
})();
