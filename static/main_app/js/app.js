// Основной JavaScript файл для приложения

document.addEventListener('DOMContentLoaded', function() {
    // Автоматическое скрытие сообщений
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            if (alert.parentNode) {
                alert.style.transition = 'opacity 0.5s ease';
                alert.style.opacity = '0';
                setTimeout(function() {
                    if (alert.parentNode) {
                        alert.parentNode.removeChild(alert);
                    }
                }, 500);
            }
        }, 5000);
    });

    // Обработка слайдера вероятности
    const probabilitySlider = document.getElementById('id_probability');
    if (probabilitySlider) {
        const probabilityValue = document.createElement('span');
        probabilityValue.className = 'ms-2 badge bg-primary';
        probabilityValue.textContent = probabilitySlider.value + '%';
        probabilitySlider.parentNode.appendChild(probabilityValue);

        probabilitySlider.addEventListener('input', function() {
            probabilityValue.textContent = this.value + '%';
        });
    }

    // Инициализация тултипов Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
