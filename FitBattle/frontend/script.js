document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('registerForm');
  const usuario = document.getElementById('usuario');
  const email = document.getElementById('email');
  const senha = document.getElementById('senha');
  const confirmaSenha = document.getElementById('confirmaSenha');
  const errorMessage = document.getElementById('errorMessage');

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    errorMessage.textContent = '';

    // Campo usuário vazio
    if (usuario.value.trim() === '') {
      showError('Por favor, informe seu nome de usuário.');
      usuario.focus();
      return;
    }

    // Validação simples de email
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email.value.trim())) {
      showError('Por favor, informe um email válido.');
      email.focus();
      return;
    }

    // Senha com no mínimo 8 caracteres
    if (senha.value.length < 8) {
      showError('A senha deve ter no mínimo 8 caracteres.');
      senha.focus();
      return;
    }

    // Confirmação de senha
    if (senha.value !== confirmaSenha.value) {
      showError('As senhas não coincidem.');
      confirmaSenha.focus();
      return;
    }

    cadastrarUsuario({
      usuario: usuario.value.trim(),
      email: email.value.trim(),
      senha: senha.value,
      confirmaSenha: confirmaSenha.value
    });
  });

  function showError(message) {
    errorMessage.textContent = message;
  }

  function cadastrarUsuario(dados) {
    fetch('/api/cadastro', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
      body: JSON.stringify(dados)
    })
      .then(function (resposta) {
        return resposta.json().then(function (corpo) {
          if (!resposta.ok) throw new Error(corpo.erro || 'Não foi possível concluir o cadastro.');
          return corpo;
        });
      })
      .then(function () {
        window.location.href = '/app';
      })
      .catch(function (erro) {
        showError(erro.message);
      });
  }
});