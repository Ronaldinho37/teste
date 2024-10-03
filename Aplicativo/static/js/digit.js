document.addEventListener("DOMContentLoaded", function() {
    // Variáveis de configuração
    const fullText = "Escola de Ensino Fundamental e Médio ";
    const highlightedText = "ANTONIO DOS SANTOS NEVES";
    const typingSpeed = 80;

    // Elementos do DOM
    const typewriterElement = document.getElementById("typewriter");
    const highlightElement = document.getElementById("highlight");
    const cursorElement = document.getElementById("cursor");
    const form = document.getElementById("carai");
    const welcomeMessage = document.getElementById("welcome-message");
    const buttonContainer = document.getElementById("button-container");
    const backButton = document.getElementById("back-button");
    const logo = document.getElementById("minha_logo");
    const emailInput = document.getElementById("nome");
    const passwordInput = document.getElementById("password");
    const errorMessage = document.getElementById("error-message");
    const confirmButton = document.getElementById("confirm-button");
    const pleaseMessage = document.getElementById("please");

    // Função para animar o texto de digitação
    function typeWriter() {
        let index = 0;
        const totalLength = fullText.length + highlightedText.length;

        function type() {
            if (index < fullText.length) {
                typewriterElement.textContent += fullText.charAt(index);
            } else if (index < totalLength) {
                highlightElement.textContent += highlightedText.charAt(index - fullText.length);
            } else {
                cursorElement.style.display = "none"; // Esconde o cursor ao finalizar
                return; // Sai da função quando terminar
            }
            index++;
            setTimeout(type, typingSpeed);
        }

        type(); // Inicia a animação
    }

    // Função para ocultar elementos e exibir botões
    function hideAndShowButtons() {
        welcomeMessage.style.transition = "opacity 0.5s ease";
        pleaseMessage.style.transition = "opacity 0.5s ease";
        form.style.transition = "opacity 0.5s ease";
        logo.style.transition = "opacity 0.5s ease";

        logo.style.opacity = "0";
        form.style.opacity = "0";
        welcomeMessage.style.opacity = "0";
        pleaseMessage.style.opacity = "0";

        // Remova os elementos completamente após a animação
        setTimeout(() => {
            welcomeMessage.style.display = "none";
            form.style.display = "none";
            
            // Mostrar os botões com fade in
            buttonContainer.style.display = "flex";
            buttonContainer.style.gap = "24px";
            buttonContainer.style.transition = "opacity 0.5s ease";
            buttonContainer.style.opacity = "0";

            setTimeout(() => {
                buttonContainer.style.opacity = "1"; // Faz o fade in dos botões
            }, 100); // Pequeno atraso para aplicar o fade in
        }, 500); // Aguarde o tempo da animação de desaparecimento
    }

    // Função de validação do formulário
    function validateForm(event) {
        event.preventDefault(); // Impede o envio do formulário para realizar validações
        errorMessage.style.display = "none"; // Limpa mensagens de erro anteriores

        const emailValid = emailInput.value !== "";
        const passwordValid = passwordInput.value !== "";

        if (!emailValid || !passwordValid) {
            errorMessage.style.display = "block"; // Mostra mensagem de erro
        } else {
            logo.style.display = "none"; // Oculta a logo
            hideAndShowButtons(); // Oculta mensagem de boas-vindas e formulário, exibe botões
        }
    }

    // Adiciona os eventos
    confirmButton.addEventListener("click", validateForm);
    backButton.addEventListener("click", function() {
        buttonContainer.style.transition = "opacity 0.5s ease";
        buttonContainer.style.opacity = "0";

        setTimeout(() => {
            buttonContainer.style.display = "none"; // Oculta o contêiner de botões
            welcomeMessage.style.display = "block"; // Mostra novamente a mensagem de boas-vindas
            pleaseMessage.style.display = "block";
            form.style.display = "block"; // Mostra novamente o formulário
            
            // Faz o fade in do formulário, da mensagem e da logo
            logo.style.opacity = "0"; // Oculta a logo inicialmente
            logo.style.display = "block"; // Garante que a logo esteja visível
            welcomeMessage.style.opacity = "0"; // Oculta a mensagem
            pleaseMessage.style.opacity = "0";
            form.style.opacity = "0"; // Oculta o formulário

            // Aplica o fade in para a logo, mensagem e formulário
            setTimeout(() => {
                logo.style.transition = "opacity 0.5s ease";
                welcomeMessage.style.transition = "opacity 0.5s ease";
                pleaseMessage.style.transition = "opacity 0.5s ease";
                form.style.transition = "opacity 0.5s ease";

                logo.style.opacity = "1"; // Aplica fade in na logo
                welcomeMessage.style.opacity = "1"; // Aplica fade in na mensagem
                pleaseMessage.style.opacity = "1"; // Aplica fade in na mensagem
                form.style.opacity = "1"; // Aplica fade in no formulário
            }, 100); // Pequeno atraso para aplicar o fade in
        }, 500); // Tempo de fade out dos botões
    });

    typeWriter(); // Inicia a animação de digitação
});