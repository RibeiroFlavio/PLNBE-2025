
const botao_musica = document.getElementById("musica");
const botao_desporto = document.getElementById("desporto");
const botao_lacos = document.getElementById("lacos");
const botao_knowledge = document.getElementById("knowledge");

const descricao_musica = document.getElementById("descricao_musica");
const descricao_desporto = document.getElementById("descricao_desporto");
const descricao_lacos = document.getElementById("descricao_lacos");
const descricao_knowledge = document.getElementById("descricao_knowledge");

botao_musica.addEventListener("click", event => {
    descricao_musica.style.display = "flex";
    descricao_desporto.style.display = "none";
    descricao_lacos.style.display = "none";
    descricao_knowledge.style.display = "none";
    window.scrollTo(0, 10000);
});

botao_desporto.addEventListener("click", event => {
    descricao_musica.style.display = "none";
    descricao_desporto.style.display = "flex";
    descricao_lacos.style.display = "none";
    descricao_knowledge.style.display = "none";
    window.scrollTo(0, 10000);
});

botao_lacos.addEventListener("click", event => {
    descricao_musica.style.display = "none";
    descricao_desporto.style.display = "none";
    descricao_lacos.style.display = "flex";
    descricao_knowledge.style.display = "none";
    window.scrollTo(0, 10000);
});

botao_knowledge.addEventListener("click", event => {
    descricao_musica.style.display = "none";
    descricao_desporto.style.display = "none";
    descricao_lacos.style.display = "none";
    descricao_knowledge.style.display = "flex";
    window.scrollTo(0, 10000);
});