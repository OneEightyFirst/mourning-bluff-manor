
(function () {
  const floorsEl = document.getElementById("floors");
  const overlay = document.getElementById("modal-overlay");
  const modalTitle = document.getElementById("modal-title");
  const modalBody = document.getElementById("modal-body");
  const modalPlotNote = document.getElementById("modal-plot-note");
  const modalRelated = document.getElementById("modal-related");
  const modalRelatedChips = document.getElementById("modal-related-chips");
  const closeBtn = document.getElementById("modal-close");

  const roomsByNum = {};
  window.ROOM_DATA.forEach(function (floor) {
    floor.rooms.forEach(function (room) {
      roomsByNum[room.num] = room;
    });
  });

  function openModal(room) {
    modalTitle.textContent = "Room " + room.num + " \u2014 " + room.name;
    modalBody.innerHTML = room.html;
    modalPlotNote.className = "modal-plot-note";
    if (room.plot) {
      modalPlotNote.hidden = false;
      modalPlotNote.textContent = room.plotNote;
      if (room.plotType) modalPlotNote.classList.add(room.plotType + "-note");
    } else {
      modalPlotNote.hidden = true;
      modalPlotNote.textContent = "";
    }

    modalRelatedChips.innerHTML = "";
    if (room.related && room.related.length) {
      modalRelated.hidden = false;
      room.related.forEach(function (rel) {
        const chip = document.createElement("button");
        chip.className = "related-chip";
        chip.type = "button";
        chip.textContent = "Room " + rel.num + " \u2014 " + rel.name;
        chip.addEventListener("click", function () {
          const target = roomsByNum[rel.num];
          if (target) openModal(target);
        });
        modalRelatedChips.appendChild(chip);
      });
    } else {
      modalRelated.hidden = true;
    }

    modalBody.querySelectorAll("a.room-link").forEach(function (a) {
      a.addEventListener("click", function (e) {
        e.preventDefault();
        const target = roomsByNum[a.dataset.room];
        if (target) openModal(target);
      });
    });

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
      btn.className = "room-btn" + (room.plotType ? " " + room.plotType + "-room" : "");
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
