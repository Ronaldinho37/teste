document.addEventListener('DOMContentLoaded', function() {
    const menuBtn = document.getElementById('menu-btn');
    const closeBtn = document.getElementById('close-btn');
    const sideNav = document.getElementById('side-nav');
    const overlay = document.getElementById('overlay');
    const themeSwitcher = document.getElementById('theme-switcher');
    const dropdownButtons = document.querySelectorAll('.dropdown-btn');

    menuBtn.addEventListener('click', function() {
        sideNav.style.left = '0';
        overlay.classList.add('show');
    });

    closeBtn.addEventListener('click', function() {
        sideNav.style.left = '-250px';
        overlay.classList.remove('show');
    });

    overlay.addEventListener('click', function() {
        sideNav.style.left = '-250px';
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
