document.addEventListener('DOMContentLoaded', function() {
    const effect = document.getElementById('effect');
    const sobreLink = document.getElementById('sobre');

    if (sobreLink) {
        sobreLink.addEventListener('click', function(event) {
            event.preventDefault(); // Previne o comportamento padrão do link

            // Adiciona a classe 'visible' ao efeito para ativar o efeito de fade-in
            effect.classList.add('visible');

            // Redireciona após o efeito de fade-in
            setTimeout(function() {
                window.location.href = sobreLink.href;
            }, 800); // Tempo deve corresponder à duração do efeito de fade-in

            // Remove a classe 'visible' após a transição para permitir o fade-out
            effect.addEventListener('transitionend', function() {
                effect.classList.remove('visible');
            });
        });
    }
});