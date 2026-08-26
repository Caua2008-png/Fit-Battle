document.addEventListener('DOMContentLoaded', function () {
  var form = document.getElementById('loginForm');
  var identificador = document.getElementById('identificador');
  var senha = document.getElementById('senha');
  var errorMessage = document.getElementById('errorMessage');

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    errorMessage.textContent = '';

    fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
      body: JSON.stringify({
        identificador: identificador.value.trim(),
        senha: senha.value
      })
    })
      .then(function (resposta) {
        return resposta.json().then(function (corpo) {
          if (!resposta.ok) throw new Error(corpo.erro || 'Não foi possível entrar.');
          return corpo;
        });
      })
      .then(function () {
        window.location.href = '/app';
      })
      .catch(function (erro) {
        errorMessage.textContent = erro.message;
      });
  });
});
