const textElement = document.getElementById('typed-text');
const phrases = ['Desenvolvedor Web', 'Programador', 'Criador de Conteúdo', 'Entusiasta de Tecnologia'];
const typingSpeed = 100; // Velocidade de digitação em milissegundos
const erasingSpeed = 50; // Velocidade de apagamento em milissegundos
const delayBetweenPhrases = 1500; // Tempo de espera entre frases em milissegundos

let currentPhraseIndex = 0;
let currentCharIndex = 0;
let isErasing = false;

function type() {
    const currentPhrase = phrases[currentPhraseIndex];
    if (!isErasing) {
        if (currentCharIndex < currentPhrase.length) {
            textElement.textContent += currentPhrase.charAt(currentCharIndex);
            currentCharIndex++;
            setTimeout(type, typingSpeed);
        } else {
            isErasing = true;
            setTimeout(type, delayBetweenPhrases);
        }
    } else {
        if (currentCharIndex > 0) {
            textElement.textContent = currentPhrase.substring(0, currentCharIndex - 1);
            currentCharIndex--;
            setTimeout(type, erasingSpeed);
        } else {
            isErasing = false;
            currentPhraseIndex = (currentPhraseIndex + 1) % phrases.length;
            setTimeout(type, delayBetweenPhrases);
        }
    }
}

// Iniciar o efeito de digitação quando a página carregar
window.onload = () => {
    type();
};
