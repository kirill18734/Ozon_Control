(function () {
  const targetText = "Угги";
  const classPrefix = "_element";

  function removeTargetDivs() {
    document.querySelectorAll(`div[class^="${classPrefix}"]`).forEach(div => {
      if (div.textContent.includes(targetText)) {
        div.remove();
        console.log("Удалён элемент с текстом 'Угги':", div);
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
