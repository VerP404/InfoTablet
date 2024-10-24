if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/service-worker.js')
            .then(registration => {
                console.log('Сервис-воркер зарегистрирован:', registration.scope);
            })
            .catch(err => {
                console.log('Ошибка при регистрации сервис-воркера:', err);
            });
    });
}
