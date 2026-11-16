// 1. Находим все кнопки меню и контейнер для контента
const menuItems = document.querySelectorAll('.menu-item');
const pageContent = document.querySelector('#page-content');
const viewDashboard = document.querySelector('#view-dashboard');

// Сохраняем оригинальный HTML дашборда в переменную, чтобы потом вернуть его обратно
const dashboardHTML = viewDashboard.innerHTML;

// 2. Логика переключения вкладок
menuItems.forEach(item => {
  item.addEventListener('click', () => {
    // Убираем класс active у всех кнопок
    menuItems.forEach(btn => btn.classList.remove('active'));
    // Добавляем класс active на ту, по которой кликнули
    item.classList.add('active');

    // Узнаем, какую страницу надо показать
    const pageName = item.getAttribute('data-page');
    
    // Меняем контент
    showPage(pageName);
  });
});

function showPage(pageName) {
  // Если выбрали Дашборд — показываем оригинальную верстку
  if (pageName === 'dashboard') {
    pageContent.innerHTML = dashboardHTML;
  } else {
    // Для всех остальных вкладок делаем простую заглушку
    pageContent.innerHTML = `
      <div class="card" style="text-align: center; padding: 50px; min-height: 400px;">
        <h2>Страница в разработке</h2>
        <p style="margin-top: 10px; color: #666;">Раздел "${pageName}" скоро появится здесь.</p>
      </div>
    `;
  }
}
