(function () {
  "use strict";

  var perfilAtual = null;
  var buscaTimer = null;

  function api(caminho, opcoes) {
    opcoes = opcoes || {};
    opcoes.credentials = "same-origin";
    return fetch("/api" + caminho, opcoes).then(function (resposta) {
      if (resposta.status === 401) {
        window.location.href = "/login";
        return Promise.reject(new Error("Não autenticado"));
      }
      return resposta.json().then(function (dados) {
        if (!resposta.ok) {
          throw new Error(dados.erro || "Erro inesperado");
        }
        return dados;
      });
    });
  }

  function catIcon(cat) {
    if (cat === "musculacao") return { icon: "ti-barbell", cls: "musculacao" };
    if (cat === "cardio") return { icon: "ti-run", cls: "cardio" };
    if (cat === "yoga") return { icon: "ti-yoga", cls: "yoga" };
    return { icon: "ti-activity", cls: "outro" };
  }

  function timeAgo(isoTime) {
    var diff = Date.now() - new Date(isoTime).getTime();
    var h = Math.floor(diff / 3600000);
    if (h < 1) return "Agora";
    if (h < 24) return "Hoje, " + new Date(isoTime).toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" });
    if (h < 48) return "Ontem, " + new Date(isoTime).toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" });
    return Math.floor(h / 24) + "d atrás";
  }

  function fmtWeight(kg, unitLb) {
    if (kg === null || kg === undefined) return "—";
    if (unitLb) return Math.round(kg * 2.2046) + "lb";
    return kg + "kg";
  }

  function showToast(msg) {
    var t = document.getElementById("toast");
    document.getElementById("toastMsg").textContent = msg;
    t.classList.add("show");
    setTimeout(function () { t.classList.remove("show"); }, 2200);
  }

  function openOverlay(id) { document.getElementById(id).classList.add("open"); }
  function closeOverlay(id) { document.getElementById(id).classList.remove("open"); }

  function avatarStyle(el, src) {
    if (src) { el.style.backgroundImage = "url(" + src + ")"; }
    else { el.style.backgroundImage = "none"; }
  }

  function renderProfile(perfil) {
    document.getElementById("pName").textContent = perfil.nome;
    document.getElementById("pSub").textContent = perfil.handle + "  ·  " + (perfil.localizacao || "");
    document.getElementById("pBio").textContent = perfil.bio || "";
    document.getElementById("statTreinos").textContent = perfil.totalTreinos;
    document.getElementById("statRank").textContent = perfil.rankingPosicao ? perfil.rankingPosicao + "º" : "—";
    document.getElementById("statStreak").textContent = perfil.streak + "d";
    document.getElementById("pWeight").textContent = fmtWeight(perfil.peso, perfil.configuracoes.unitLb);
    document.getElementById("pHeight").textContent = perfil.altura != null ? perfil.altura.toFixed(2).replace(".", ",") : "—";
    document.getElementById("pAge").textContent = perfil.idade != null ? perfil.idade : "—";
    avatarStyle(document.getElementById("avatarBtn"), perfil.avatar);
    avatarStyle(document.getElementById("navAvatar"), perfil.avatar);

    document.getElementById("levelName").textContent = perfil.nivel.nome;
    document.getElementById("levelFill").style.width = perfil.nivel.percentual + "%";
    document.getElementById("levelMarker").style.left = perfil.nivel.percentual + "%";
    document.getElementById("levelArrow").style.left = perfil.nivel.percentual + "%";
    document.getElementById("levelRemaining").textContent = "Faltam " + perfil.nivel.restante + "xp para o próximo nível";

    bindToggle("toggleUnit", perfil.configuracoes.unitLb, "unitLb");
    bindToggle("toggleNotif", perfil.configuracoes.notif, "notif");
    bindToggle("togglePublic", perfil.configuracoes.publicRanking, "publicRanking");
  }

  function cardHTML(c) {
    var head = "";
    if (c.tipo === "treino") {
      var ci = catIcon(c.categoria);
      head = '<div class="card-icon ' + ci.cls + '"><i class="ti ' + ci.icon + '" aria-hidden="true"></i></div>' +
        '<div><div class="card-title">' + c.titulo + '  <span>- ' + c.grupo + '</span></div></div>';
    } else {
      head = '<div class="card-icon post"><i class="ti ti-message-2" aria-hidden="true"></i></div>' +
        '<div><div class="card-title">' + c.usuarioNome + '</div></div>';
    }

    var statsHTML = "";
    if (c.tipo === "treino") {
      statsHTML = '<div class="card-stats">' + c.estatisticas.map(function (s) {
        return '<div class="cs"><b>' + s.valor + '<small>' + s.unidade + '</small></b><span>' + s.rotulo + '</span></div>';
      }).join("") + '</div>';
    }

    var photoHTML = c.foto ? '<img class="card-photo" src="' + c.foto + '" alt="Foto da postagem">' : "";
    var canDelete = c.usuarioId === perfilAtual.id;

    return '<article class="card" data-id="' + c.id + '">' +
      '<div class="card-head"><div class="card-head-left">' + head + '</div><span class="card-time">' + timeAgo(c.criadoEm) + '</span></div>' +
      '<p class="card-body">' + c.descricao + '</p>' +
      photoHTML + statsHTML +
      '<div class="card-actions">' +
      '<button class="pill-btn" data-action="share" data-id="' + c.id + '"><i class="ti ti-share-3" aria-hidden="true"></i>Compartilhar</button>' +
      (canDelete ? '<button class="pill-btn danger" data-action="delete" data-id="' + c.id + '"><i class="ti ti-trash" aria-hidden="true"></i>Excluir</button>' : '') +
      '</div>' +
      '</article>';
  }

  function carregarFeed() {
    var busca = document.getElementById("searchInput").value.trim();
    var query = busca ? "?busca=" + encodeURIComponent(busca) : "";
    return api("/feed" + query).then(function (lista) {
      var feed = document.getElementById("feed");
      if (lista.length === 0) {
        feed.innerHTML = '<p class="feed-empty">Nenhum conteúdo encontrado. Toque em "+" para criar seu primeiro treino ou postagem.</p>';
        return;
      }
      feed.innerHTML = lista.map(cardHTML).join("");
    });
  }

  function carregarPerfil() {
    return api("/perfil").then(function (perfil) {
      perfilAtual = perfil;
      renderProfile(perfil);
    });
  }

  function recarregarTudo() {
    return Promise.all([carregarPerfil(), carregarFeed()]);
  }

  function bindToggle(id, valorAtual, chave) {
    var el = document.getElementById(id);
    el.classList.toggle("on", !!valorAtual);
    el.onclick = function () {
      var novoValor = !el.classList.contains("on");
      el.classList.toggle("on", novoValor);
      var corpo = {};
      corpo[chave] = novoValor;
      api("/perfil/configuracoes", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(corpo)
      }).then(function () {
        if (chave === "unitLb") carregarPerfil();
      });
    };
  }

  function openProfileEdit() {
    var p = perfilAtual;
    document.getElementById("editName").value = p.nome;
    document.getElementById("editHandle").value = p.handle;
    document.getElementById("editLocation").value = p.localizacao || "";
    document.getElementById("editBio").value = p.bio || "";
    document.getElementById("editWeight").value = p.peso != null ? p.peso : "";
    document.getElementById("editHeight").value = p.altura != null ? p.altura : "";
    document.getElementById("editAge").value = p.idade != null ? p.idade : "";
    document.getElementById("erroProfile").textContent = "";
    avatarStyle(document.getElementById("editAvatarPreview"), p.avatar);
    openOverlay("overlayProfile");
  }

  function init() {
    document.getElementById("homeBtn").addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });

    document.getElementById("searchInput").addEventListener("input", function () {
      clearTimeout(buscaTimer);
      buscaTimer = setTimeout(carregarFeed, 250);
    });

    document.getElementById("fabBtn").addEventListener("click", function () { openOverlay("overlayChoice"); });
    document.getElementById("closeChoice").addEventListener("click", function () { closeOverlay("overlayChoice"); });
    document.getElementById("choiceTreino").addEventListener("click", function () { closeOverlay("overlayChoice"); openOverlay("overlayTreino"); });
    document.getElementById("choicePost").addEventListener("click", function () { closeOverlay("overlayChoice"); openOverlay("overlayPost"); });
    document.getElementById("closeTreino").addEventListener("click", function () { closeOverlay("overlayTreino"); });
    document.getElementById("closePost").addEventListener("click", function () { closeOverlay("overlayPost"); });

    var catSelect = document.getElementById("treinoCategoria");
    catSelect.addEventListener("change", function () {
      var s2 = document.getElementById("s2Label"), s3 = document.getElementById("s3Label");
      if (catSelect.value === "cardio") { s2.textContent = "Velocidade (km/h)"; s3.textContent = "Inclinação"; }
      else { s2.textContent = "Carga máx. (kg)"; s3.textContent = "Séries"; }
    });

    document.getElementById("formTreino").addEventListener("submit", function (e) {
      e.preventDefault();
      var corpo = {
        categoria: catSelect.value,
        grupo: document.getElementById("treinoGrupo").value.trim(),
        descricao: document.getElementById("treinoDesc").value.trim(),
        duracao: document.getElementById("s1v").value,
        metrica2: document.getElementById("s2v").value,
        metrica3: document.getElementById("s3v").value
      };
      api("/treinos", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(corpo)
      }).then(function () {
        e.target.reset();
        closeOverlay("overlayTreino");
        showToast("Treino publicado!");
        recarregarTudo();
      }).catch(function (erro) {
        document.getElementById("erroTreino").textContent = erro.message;
      });
    });

    document.getElementById("formPost").addEventListener("submit", function (e) {
      e.preventDefault();
      var formData = new FormData();
      formData.append("texto", document.getElementById("postTexto").value.trim());
      var fotoInput = document.getElementById("postFoto");
      if (fotoInput.files[0]) formData.append("foto", fotoInput.files[0]);

      api("/postagens", { method: "POST", body: formData }).then(function () {
        e.target.reset();
        closeOverlay("overlayPost");
        showToast("Postagem publicada!");
        recarregarTudo();
      }).catch(function (erro) {
        document.getElementById("erroPost").textContent = erro.message;
      });
    });

    document.getElementById("feed").addEventListener("click", function (e) {
      var btn = e.target.closest("[data-action]");
      if (!btn) return;
      var id = btn.getAttribute("data-id");
      var action = btn.getAttribute("data-action");
      var partes = id.split("-");
      var tipo = partes[0];
      var itemId = partes[1];

      if (action === "share") {
        var url = window.location.href.split("#")[0] + "#" + id;
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(url).then(function () { showToast("Link copiado!"); }).catch(function () { showToast("Não foi possível copiar o link"); });
        } else {
          showToast("Link: " + url);
        }
      } else if (action === "delete") {
        api("/cards/" + tipo + "/" + itemId, { method: "DELETE" }).then(function () {
          showToast("Publicação excluída");
          recarregarTudo();
        });
      }
    });

    document.getElementById("editProfileBtn").addEventListener("click", openProfileEdit);
    document.getElementById("navAvatar").addEventListener("click", openProfileEdit);
    document.getElementById("closeProfile").addEventListener("click", function () { closeOverlay("overlayProfile"); });

    document.getElementById("avatarBtn").addEventListener("click", openProfileEdit);
    document.getElementById("avatarFileBtn").addEventListener("click", function () { document.getElementById("avatarFile").click(); });
    document.getElementById("avatarFile").addEventListener("change", function () {
      var file = this.files[0];
      if (!file) return;
      var preview = new FileReader();
      preview.onload = function (e) { avatarStyle(document.getElementById("editAvatarPreview"), e.target.result); };
      preview.readAsDataURL(file);

      var formData = new FormData();
      formData.append("avatar", file);
      api("/perfil/avatar", { method: "POST", body: formData }).then(function () {
        showToast("Avatar atualizado");
        carregarPerfil();
      });
    });

    document.getElementById("formProfile").addEventListener("submit", function (e) {
      e.preventDefault();
      var corpo = {
        nome: document.getElementById("editName").value.trim(),
        handle: document.getElementById("editHandle").value.trim(),
        localizacao: document.getElementById("editLocation").value.trim(),
        bio: document.getElementById("editBio").value.trim(),
        peso: document.getElementById("editWeight").value,
        altura: document.getElementById("editHeight").value,
        idade: document.getElementById("editAge").value
      };
      api("/perfil", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(corpo)
      }).then(function () {
        closeOverlay("overlayProfile");
        showToast("Perfil atualizado");
        carregarPerfil();
      }).catch(function (erro) {
        document.getElementById("erroProfile").textContent = erro.message;
      });
    });

    document.getElementById("btnRanking").addEventListener("click", function () {
      api("/ranking").then(function (lista) {
        document.getElementById("rankingList").innerHTML = lista.map(function (r) {
          var souEu = r.id === perfilAtual.id;
          return '<div class="rank-row ' + (souEu ? 'me' : '') + '">' +
            '<span class="pos">' + r.posicao + 'º</span>' +
            '<span class="avatar-mini" style="' + (r.avatar ? 'background-image:url(' + r.avatar + ')' : '') + '"></span>' +
            '<span class="name">' + r.nome + (souEu ? ' (você)' : '') + '</span>' +
            '<span class="xp">' + r.xp.toLocaleString("pt-BR") + ' xp</span>' +
            '</div>';
        }).join("");
        openOverlay("overlayRanking");
      });
    });
    document.getElementById("closeRanking").addEventListener("click", function () { closeOverlay("overlayRanking"); });

    document.getElementById("btnProgress").addEventListener("click", function () {
      var p = perfilAtual;
      var rows = [
        ["Treinos registrados", p.totalTreinos],
        ["Postagens", p.totalPostagens],
        ["Sequência atual", p.streak + " dias"],
        ["XP total", p.xp.toLocaleString("pt-BR")],
        ["Nível atual", p.nivel.nome],
        ["Progresso no nível", p.nivel.percentual + "%"]
      ];
      document.getElementById("progressList").innerHTML = rows.map(function (r) {
        return '<div class="prow"><span>' + r[0] + '</span><span>' + r[1] + '</span></div>';
      }).join("");
      openOverlay("overlayProgress");
    });
    document.getElementById("closeProgress").addEventListener("click", function () { closeOverlay("overlayProgress"); });

    document.getElementById("btnSettings").addEventListener("click", function () { openOverlay("overlaySettings"); });
    document.getElementById("closeSettings").addEventListener("click", function () { closeOverlay("overlaySettings"); });

    document.getElementById("btnLogout").addEventListener("click", function () {
      api("/logout", { method: "POST" }).then(function () {
        window.location.href = "/login";
      });
    });

    document.querySelectorAll(".overlay").forEach(function (ov) {
      ov.addEventListener("click", function (e) { if (e.target === ov) ov.classList.remove("open"); });
    });

    recarregarTudo();
  }

  document.addEventListener("DOMContentLoaded", init);
})();
