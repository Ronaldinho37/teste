
document.addEventListener("DOMContentLoaded", function() {
    const eletivaElement = document.querySelector("#tecnologia strong");
    const cursorElement = document.querySelector(".cursor");
    const palavras = ["Programação", "Desenvolvimento Web", "Design", "Full-stack"]; // Palavras a serem digitadas
    let palavraIndex = 0;
    let letraIndex = 0;

    function digitarPalavra() {
        if (letraIndex < palavras[palavraIndex].length) {
            eletivaElement.textContent += palavras[palavraIndex].charAt(letraIndex);
            letraIndex++;
            setTimeout(digitarPalavra, 150); // Atraso entre cada letra (150ms)
        } else {
            setTimeout(apagarPalavra, 1000); // Atraso antes de apagar a palavra (1000ms)
        }
    }

    function apagarPalavra() {
        if (letraIndex > 0) {
            eletivaElement.textContent = palavras[palavraIndex].substring(0, letraIndex - 1);
            letraIndex--;
            setTimeout(apagarPalavra, 100); // Atraso entre cada letra ao apagar (100ms)
        } else {
            palavraIndex = (palavraIndex + 1) % palavras.length;
            setTimeout(digitarPalavra, 500); // Atraso antes de iniciar a próxima palavra (500ms)
        }
    }

    digitarPalavra();
});


   