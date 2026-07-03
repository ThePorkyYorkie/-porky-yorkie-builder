const DEFAULT_POSITIONS = {
  "Item Name": {
    "x": 50,
    "y": 20,
    "size": 24,
    "align": "center"
  },
  "Tagged Size": {
    "x": 50,
    "y": 26,
    "size": 24,
    "align": "center"
  },
  "Pit to Pit": {
    "x": 42,
    "y": 43,
    "size": 34,
    "align": "center"
  },
  "Length": {
    "x": 58,
    "y": 52,
    "size": 34,
    "align": "center"
  },
  "Sleeve Length": {
    "x": 75,
    "y": 43,
    "size": 32,
    "align": "center"
  },
  "Waist": {
    "x": 50,
    "y": 49,
    "size": 30,
    "align": "center"
  },
  "Rise": {
    "x": 52,
    "y": 45,
    "size": 30,
    "align": "center"
  },
  "Inseam": {
    "x": 46,
    "y": 58,
    "size": 30,
    "align": "center"
  },
  "Outseam": {
    "x": 70,
    "y": 56,
    "size": 30,
    "align": "center"
  },
  "Leg Opening": {
    "x": 52,
    "y": 70,
    "size": 30,
    "align": "center"
  },
  "Thigh": {
    "x": 45,
    "y": 52,
    "size": 30,
    "align": "center"
  },
  "Overall Length": {
    "x": 66,
    "y": 45,
    "size": 30,
    "align": "center"
  },
  "Shoulder": {
    "x": 48,
    "y": 35,
    "size": 30,
    "align": "center"
  },
  "Jacket Pit to Pit": {
    "x": 35,
    "y": 40,
    "size": 28,
    "align": "center"
  },
  "Jacket Waist": {
    "x": 40,
    "y": 48,
    "size": 28,
    "align": "center"
  },
  "Jacket Length": {
    "x": 58,
    "y": 55,
    "size": 28,
    "align": "center"
  },
  "Pant Waist": {
    "x": 72,
    "y": 42,
    "size": 28,
    "align": "center"
  },
  "Vest Pit to Pit": {
    "x": 50,
    "y": 42,
    "size": 28,
    "align": "center"
  },
  "Vest Length": {
    "x": 55,
    "y": 55,
    "size": 28,
    "align": "center"
  }
};

let templates = [];
let currentTemplate = null;
let values = {};
let positions = {};
let calibrating = false;

const $ = (id) => document.getElementById(id);

async function init() {
  try {
    const response = await fetch("templates.json", { cache: "no-store" });
    templates = await response.json();
  } catch (err) {
    alert("Could not load templates.json. Make sure it is uploaded to GitHub.");
    console.error(err);
    return;
  }

  buildTemplateSelect();
  await loadTemplate(templates[0].id);
}

function buildTemplateSelect() {
  const select = $("templateSelect");
  select.innerHTML = "";
  templates.forEach((template) => {
    const option = document.createElement("option");
    option.value = template.id;
    option.textContent = template.label;
    select.appendChild(option);
  });

  select.addEventListener("change", async () => {
    await loadTemplate(select.value);
  });
}

async function loadTemplate(id) {
  currentTemplate = templates.find((t) => t.id === id);
  values = {};
  positions = loadPositions(currentTemplate.id);

  $("templateSelect").value = id;

  const imagePath = `templates/${currentTemplate.file}`;
  const img = $("templateImg");
  img.crossOrigin = "anonymous";
  img.src = imagePath;
  img.onerror = () => {
    $("templateStatus").innerHTML = `<span class="missing">❌ Missing template image: templates/${currentTemplate.file}</span>`;
  };
  img.onload = () => {
    $("templateStatus").innerHTML = `<span class="loaded">✅ Loaded: ${currentTemplate.label}</span>`;
    renderOverlay();
  };

  renderFields();
  renderOverlay();
}

function loadPositions(templateId) {
  const saved = localStorage.getItem(`py_positions_${templateId}`);
  if (saved) {
    try { return JSON.parse(saved); } catch {}
  }

  const pos = {};
  currentTemplate.fields.forEach((field) => {
    pos[field] = { ...(DEFAULT_POSITIONS[field] || { x: 50, y: 50, size: 28, align: "center" }) };
  });
  return pos;
}

function savePositions() {
  localStorage.setItem(`py_positions_${currentTemplate.id}`, JSON.stringify(positions));
  alert(`Saved text positions for ${currentTemplate.label}`);
}

function resetPositions() {
  if (!confirm("Reset text positions for this template?")) return;
  localStorage.removeItem(`py_positions_${currentTemplate.id}`);
  positions = loadPositions(currentTemplate.id);
  renderOverlay();
}

function renderFields() {
  const fields = $("fields");
  fields.innerHTML = "";

  currentTemplate.fields.forEach((field) => {
    const label = document.createElement("label");
    label.textContent = field;

    const input = document.createElement("input");
    input.placeholder = field;
    input.value = values[field] || "";
    input.addEventListener("input", () => {
      values[field] = input.value;
      renderOverlay();
    });

    fields.appendChild(label);
    fields.appendChild(input);
  });
}

function isMeasurementField(field) {
  return !["Item Name", "Tagged Size"].includes(field);
}

function formatField(field, value) {
  value = String(value || "").trim();
  if (!value) return "";
  if (isMeasurementField(field) && !value.endsWith('"')) return `${value}"`;
  return value;
}

function renderOverlay() {
  const overlayLayer = $("overlayLayer");
  const previewWrap = $("previewWrap");
  overlayLayer.innerHTML = "";

  previewWrap.classList.toggle("calibrating", calibrating);
  if (!currentTemplate) return;

  currentTemplate.fields.forEach((field) => {
    const pos = positions[field] || { x: 50, y: 50, size: 28, align: "center" };
    const value = formatField(field, values[field]);

    if (!value && !calibrating) return;

    const div = document.createElement("div");
    div.className = "overlay";
    div.dataset.field = field;
    div.textContent = value || field;
    div.style.left = `${pos.x}%`;
    div.style.top = `${pos.y}%`;
    div.style.fontSize = `${Math.max(11, previewWrap.clientWidth * ((pos.size || 28) / 1254))}px`;
    div.style.opacity = value ? "1" : ".58";
    div.style.textAlign = pos.align || "center";

    if (calibrating) makeDraggable(div, field);

    overlayLayer.appendChild(div);
  });
}

function makeDraggable(element, field) {
  let dragging = false;

  function updatePosition(clientX, clientY) {
    const rect = $("previewWrap").getBoundingClientRect();
    positions[field].x = Math.max(0, Math.min(100, ((clientX - rect.left) / rect.width) * 100));
    positions[field].y = Math.max(0, Math.min(100, ((clientY - rect.top) / rect.height) * 100));
    element.style.left = `${positions[field].x}%`;
    element.style.top = `${positions[field].y}%`;
  }

  element.addEventListener("pointerdown", (event) => {
    dragging = true;
    element.setPointerCapture(event.pointerId);
    updatePosition(event.clientX, event.clientY);
  });

  element.addEventListener("pointermove", (event) => {
    if (dragging) updatePosition(event.clientX, event.clientY);
  });

  element.addEventListener("pointerup", () => {
    dragging = false;
  });
}

function toggleCalibrate() {
  calibrating = !calibrating;
  $("calibrateBtn").textContent = calibrating ? "Turn Off Position Adjust Mode" : "Turn On Position Adjust Mode";
  $("savePositionsBtn").classList.toggle("hidden", !calibrating);
  renderOverlay();
}

function clearFields() {
  values = {};
  renderFields();
  renderOverlay();
}

function exportPNG() {
  const img = $("templateImg");

  if (!img.complete || img.naturalWidth === 0) {
    alert("Template image is missing or still loading.");
    return;
  }

  const canvas = document.createElement("canvas");
  canvas.width = img.naturalWidth;
  canvas.height = img.naturalHeight;

  const ctx = canvas.getContext("2d");
  ctx.drawImage(img, 0, 0);

  currentTemplate.fields.forEach((field) => {
    const value = formatField(field, values[field]);
    if (!value) return;

    const pos = positions[field] || { x: 50, y: 50, size: 28, align: "center" };
    const size = Math.round((pos.size || 28) * (canvas.width / 1254));

    ctx.fillStyle = "#061b3a";
    ctx.font = `900 ${size}px Arial, sans-serif`;
    ctx.textAlign = pos.align || "center";
    ctx.textBaseline = "middle";
    ctx.fillText(value, (pos.x / 100) * canvas.width, (pos.y / 100) * canvas.height);
  });

  const filenameBase = (values["Item Name"] || currentTemplate.label || "measurement-guide")
    .replace(/[^a-z0-9]+/gi, "-")
    .replace(/^-|-$/g, "");

  const link = document.createElement("a");
  link.download = `${filenameBase}.png`;
  link.href = canvas.toDataURL("image/png");
  link.click();
}

$("exportBtn").addEventListener("click", exportPNG);
$("clearBtn").addEventListener("click", clearFields);
$("calibrateBtn").addEventListener("click", toggleCalibrate);
$("savePositionsBtn").addEventListener("click", savePositions);
$("resetPositionsBtn").addEventListener("click", resetPositions);
window.addEventListener("resize", renderOverlay);

init();
