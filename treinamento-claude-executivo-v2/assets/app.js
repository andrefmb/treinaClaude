/* =========================================================================
   Dominando o Claude — motor de interatividade
   Copiar prompts · tooltips de glossário · progresso (localStorage)
   ========================================================================= */
(function () {
  "use strict";
  var STORAGE_KEY = "treino-claude-executivo-v2-progresso";
  var ORDER = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16"];

  function loadProgress() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {}; }
    catch (e) { return {}; }
  }
  function saveProgress(p) {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(p)); } catch (e) {}
  }
  function isDone(id) { return !!loadProgress()[id]; }
  function setDone(id, val) {
    var p = loadProgress();
    if (val) p[id] = true; else delete p[id];
    saveProgress(p);
  }

  function initCopy() {
    document.querySelectorAll(".codeblock").forEach(function (block) {
      if (block.querySelector(".copy-btn")) return;
      var pre = block.querySelector("pre");
      if (!pre) return;
      var btn = document.createElement("button");
      btn.className = "copy-btn"; btn.type = "button"; btn.textContent = "Copiar";
      btn.addEventListener("click", function () {
        var text = pre.innerText;
        var done = function () {
          btn.textContent = "Copiado!"; btn.classList.add("copied");
          setTimeout(function () { btn.textContent = "Copiar"; btn.classList.remove("copied"); }, 1600);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(done, fallback);
        } else { fallback(); }
        function fallback() {
          var ta = document.createElement("textarea");
          ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0";
          document.body.appendChild(ta); ta.select();
          try { document.execCommand("copy"); done(); } catch (e) {}
          document.body.removeChild(ta);
        }
      });
      block.appendChild(btn);
    });
  }

  // reposiciona o tooltip para nunca sair da tela na horizontal
  function positionTip(t) {
    var tip = t.querySelector(".tip");
    if (!tip) return;
    var r = t.getBoundingClientRect();
    var w = tip.offsetWidth;
    var center = r.left + r.width / 2;
    var left = center - w / 2;
    var m = 10, shift = 0;
    if (left < m) shift = m - left;
    else if (left + w > window.innerWidth - m) shift = (window.innerWidth - m) - (left + w);
    shift = Math.round(shift);
    tip.style.transform = "translateX(calc(-50% + " + shift + "px)) translateY(-2px)";
    tip.style.setProperty("--arrow-shift", (-shift) + "px");
  }

  function initTooltips() {
    var terms = document.querySelectorAll(".term");
    terms.forEach(function (t) {
      t.setAttribute("tabindex", "0");
      t.addEventListener("mouseenter", function () { positionTip(t); });
      t.addEventListener("focus", function () { positionTip(t); });
      t.addEventListener("click", function (e) {
        e.stopPropagation();
        var wasOpen = t.classList.contains("open");
        terms.forEach(function (o) { o.classList.remove("open"); });
        if (!wasOpen) { t.classList.add("open"); positionTip(t); }
      });
    });
    document.addEventListener("click", function () {
      terms.forEach(function (o) { o.classList.remove("open"); });
    });
  }

  function initDoneBar() {
    var bar = document.querySelector("[data-done-bar]");
    if (!bar) return;
    var id = bar.getAttribute("data-mod");
    var btn = bar.querySelector("[data-done-btn]");
    var nextLabel = bar.getAttribute("data-next-label") || "";
    var nextHref = bar.getAttribute("data-next-href") || "";
    function render() {
      var done = isDone(id);
      bar.classList.toggle("is-done", done);
      if (done) {
        btn.textContent = nextHref ? "✓ Concluído — Próximo: " + nextLabel : "✓ Concluído";
      } else {
        btn.textContent = nextLabel ? "Marcar como concluído — Próximo: " + nextLabel : "Marcar como concluído";
      }
    }
    btn.addEventListener("click", function () {
      var done = isDone(id);
      if (!done) {
        setDone(id, true); render();
        if (nextHref) setTimeout(function () { window.location.href = nextHref; }, 550);
      } else { setDone(id, false); render(); }
    });
    render();
  }

  function initList() {
    var list = document.querySelector("[data-mod-list]");
    if (!list) return;
    var prog = loadProgress();
    var doneCount = 0;
    list.querySelectorAll("[data-mod-row]").forEach(function (row) {
      var id = row.getAttribute("data-mod-row");
      if (prog[id]) { row.classList.add("done"); doneCount++; }
      var chk = row.querySelector(".check");
      if (chk && prog[id]) chk.textContent = "✓";
    });
    var total = ORDER.length;
    var pct = Math.round((doneCount / total) * 100);
    var fill = document.querySelector("[data-progress-fill]");
    var txt = document.querySelector("[data-progress-text]");
    if (fill) fill.style.width = pct + "%";
    if (txt) txt.textContent = doneCount + " de " + total + " módulos concluídos (" + pct + "%)";
  }

  document.addEventListener("DOMContentLoaded", function () {
    initCopy(); initTooltips(); initDoneBar(); initList();
  });
})();
