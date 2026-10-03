
(function () {
  const floorsEl = document.getElementById("floors");
  const overlay = document.getElementById("modal-overlay");
  const modalTitle = document.getElementById("modal-title");
  const modalBody = document.getElementById("modal-body");
  const modalPlotNote = document.getElementById("modal-plot-note");
  const closeBtn = document.getElementById("modal-close");

  function openModal(room) {
    modalTitle.textContent = "Room " + room.num + " \u2014 " + room.name;
    modalBody.innerHTML = room.html;
    if (room.plot) {
      modalPlotNote.hidden = false;
      modalPlotNote.textContent = room.plotNote;
    } else {
      modalPlotNote.hidden = true;
      modalPlotNote.textContent = "";
    }
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

  window.ROOM_DATA.forEach(function (floor) {
    const section = document.createElement("section");
    section.className = "floor-section";

    const h2 = document.createElement("h2");
    h2.textContent = floor.title;
    section.appendChild(h2);

    const grid = document.createElement("div");
    grid.className = "room-grid";

    floor.rooms.forEach(function (room) {
      const btn = document.createElement("button");
      btn.className = "room-btn" + (room.plot ? " plot-item" : "");
      btn.innerHTML =
        '<span class="room-num">Room ' + room.num + '</span>' +
        '<span class="room-name">' + room.name + '</span>';
      btn.addEventListener("click", function () {
        openModal(room);
      });
      grid.appendChild(btn);
    });

    section.appendChild(grid);
    floorsEl.appendChild(section);
  });
})();
