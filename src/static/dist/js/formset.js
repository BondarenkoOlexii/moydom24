$(document).ready(function() {

    // Додавання нової форми
    $('.form-row-add-section-btn, .form-row-add-storey-btn, .form-row-add-houseuseradmins-btn, .form-row-add-service-btn, .form-row-add-measurement-btn, .form-row-add-tariffservice-btn, .form-row-add-websitedocument-btn, .form-row-add-webservice-btn').click(function(e) {
        e.preventDefault();

        console.log("Я працюю");

        // 1. Отримуємо префікс конкретного формсета з кнопки (наприклад, 'sections' або 'items')
        let prefix = $(this).data('prefix');
        console.log("Клік по кнопці з префіксом:", prefix);

        // 2. Знаходимо поле TOTAL_FORMS саме для цього формсета
        let totalFormsInput = $('#id_' + prefix + '-TOTAL_FORMS');

        // 3. Беремо поточну кількість форм
        let currentFormCount = parseInt(totalFormsInput.val());

        // 4. Беремо HTML з відповідного прихованого шаблону
        let emptyTemplateHtml = $('#empty-template-' + prefix).html();

        // 5. Замінюємо всі "__prefix__" на поточний номер (індекс нової форми)
        let compiledHtml = emptyTemplateHtml.replace(/__prefix__/g, currentFormCount);

        // 6. Додаємо згенерований HTML у відповідний контейнер
        $('#container-' + prefix).append(compiledHtml);

        // 7. Збільшуємо лічильник TOTAL_FORMS на 1
        totalFormsInput.val(currentFormCount + 1);

        // Дебаг: вивід у консоль, щоб переконатися, що все працює
        console.log(`Додано форму для '${prefix}'. Новий лічильник: ${currentFormCount + 1}`);
    });

    // Видалення форми (спрацьовує і для існуючих, і для щойно доданих)
    $('.tab-content').on('click', '.form-row-remove-btn', function(e) {
        e.preventDefault();
        console.log("Я видалення працюю");

        // УНІВЕРСАЛЬНИЙ ПОШУК: шукаємо будь-який батьківський рядок, що закінчується на "-row"
        let row = $(this).closest('[class$="-row"]');

        // Знаходимо чекбокс DELETE
        let deleteInput = row.find('input[name$="-DELETE"]');

        if (deleteInput.length > 0) {
            // Для існуючих записів у базі: ставимо галочку і ховаємо рядок
            deleteInput.prop('checked', true); // .prop('checked', true) замість .val('on')
            row.hide();
            console.log("Сховали існуючий рядок");
        } else {
            // Для нових записів (ще не збережених): просто видаляємо з HTML
            row.remove();
            console.log("Видалили новий рядок");
        }
    });

});