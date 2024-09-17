document.addEventListener('DOMContentLoaded', function() {
    const menuBtn = document.getElementById('menu-btn');
    const closeBtn = document.getElementById('close-btn');
    const sideNav = document.getElementById('side-nav');
    const effect = document.getElementById('effect');
    const themeSwitcher = document.getElementById('theme-switcher');
    const dropdownButtons = document.querySelectorAll('.dropdown-btn');

    menuBtn.addEventListener('click', function() {
        sideNav.style.right = '0'; /* Abrir o menu pela direita */
        effect.classList.remove('visible'); // Certifique-se de que o efeito está oculto
    });

    closeBtn.addEventListener('click', function() {
        sideNav.style.right = '-250px'; /* Fechar o menu pela direita */
        effect.classList.remove('visible');
    });

    // Adicione o código para ocultar o side nav e mostrar o efeito
    const sobreLink = document.getElementById('sobre');
    if (sobreLink) {
        sobreLink.addEventListener('click', function(event) {
            event.preventDefault(); // Previne o comportamento padrão do link

            // Oculta o side nav
            sideNav.style.right = '-250px';
            
            // Adiciona a classe 'visible' ao efeito para ativar o efeito de fade-in
            effect.classList.add('visible');

            // Redireciona após o efeito de fade-in
            setTimeout(function() {
                window.location.href = sobreLink.href;
            }, 3000); // Tempo deve corresponder à duração do efeito de fade-in
        });
    }

    const overlay = document.getElementById('overlay');
    menuBtn.addEventListener('click', function() {
        sideNav.style.right = '0'; /* Abrir o menu pela direita */
        overlay.classList.add('show');
    });

    closeBtn.addEventListener('click', function() {
        sideNav.style.right = '-250px'; /* Fechar o menu pela direita */
        overlay.classList.remove('show');
    });

    overlay.addEventListener('click', function() {
        sideNav.style.right = '-250px'; /* Fechar o menu pela direita */
        overlay.classList.remove('show');
    });

    themeSwitcher.addEventListener('click', function() {
        document.body.classList.toggle('dark-theme');
        themeSwitcher.textContent = document.body.classList.contains('dark-theme') ? '🌙' : '🔆';
    });

    dropdownButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); // Evita o comportamento padrão do link
            
            const targetId = button.getAttribute('data-target');
            const dropdown = document.getElementById(targetId);
            const isActive = dropdown.parentElement.classList.toggle('active');
            
            // Fecha outros drop-downs se existirem
            document.querySelectorAll('.dropdown-content').forEach(d => {
                if (d !== dropdown) {
                    d.parentElement.classList.remove('active');
                }
            });
            
            // Controla a exibição do drop-down do item clicado
            if (isActive) {
                dropdown.style.display = 'block';
            } else {
                dropdown.style.display = 'none';
            }
        });
    });

    // Fecha o drop-down se o usuário clicar fora dele
    document.addEventListener('click', function(event) {
        if (!event.target.closest('.menu-item') && !event.target.closest('.dropdown-content')) {
            document.querySelectorAll('.dropdown-content').forEach(dropdown => {
                dropdown.parentElement.classList.remove('active');
                dropdown.style.display = 'none';
            });
        }
    });
});
