
(function () {
  const grid = document.getElementById("cast-grid");
  const overlay = document.getElementById("modal-overlay");
  const modalTitle = document.getElementById("modal-title");
  const modalBody = document.getElementById("modal-body");
  const closeBtn = document.getElementById("modal-close");

  function openModal(member) {
    modalTitle.textContent = member.name;
    modalBody.innerHTML = member.html;
    overlay.hidden = false;
    closeBtn.focus();
  }

  function closeModal() {
    overlay.hidden = true;
  }

  closeBtn.addEventListener("click", closeModal);
  overlay.addEventListener("click", function (e) {
    if (e.target === overlay) closeModal();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !overlay.hidden) closeModal();
  });

  window.CAST_DATA.forEach(function (member) {
    const btn = document.createElement("button");
    btn.className = "room-btn";
    btn.innerHTML = '<span class="room-name">' + member.name + '</span>';
    btn.addEventListener("click", function () {
      openModal(member);
    });
    grid.appendChild(btn);
  });
})();
