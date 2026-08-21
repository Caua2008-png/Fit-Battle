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

    // Tudo certo - aqui você integraria com o backend
    cadastrarUsuario({
      usuario: usuario.value.trim(),
      email: email.value.trim(),
      senha: senha.value
    });
  });

  function showError(message) {
    errorMessage.textContent = message;
  }

  function cadastrarUsuario(dados) {
    console.log('Dados de cadastro:', dados);
    alert('Cadastro realizado com sucesso!');
    form.reset();
  }
});