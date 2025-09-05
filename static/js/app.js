
async function fetchEquipment(q=""){
  const url = q ? `/api/equipment?q=${encodeURIComponent(q)}` : '/api/equipment';
  const r = await fetch(url);
  return await r.json();
}

function renderList(items){
  const list = document.getElementById('list');
  list.innerHTML = items.map(e => `
    <div class="card">
      <div class="card-head">
        <h3>${e.name}</h3>
        <a class="btn" href="/equipment/${e.id}">Abrir</a>
      </div>
      <div class="grid">
        <div><b>SAP:</b> ${e.sap_number || "-"}</div>
        <div><b>Tag:</b> ${e.tag || "-"}</div>
        <div><b>Ubicación:</b> ${e.location || "-"}</div>
        <div><b>Criticidad:</b> ${e.criticality || "-"}</div>
        <div><b>Estatus:</b> ${e.status || "-"}</div>
      </div>
    </div>
  `).join("");
}

async function initial(){
  const items = await fetchEquipment();
  renderList(items);

  document.getElementById('search').addEventListener('input', async (e)=>{
    renderList(await fetchEquipment(e.target.value));
  });

  document.getElementById('btn-new').addEventListener('click', async ()=>{
    const name = prompt("Nombre del equipo:");
    if (!name) return;
    const sap = prompt("Número SAP (opcional):");
    const tag = prompt("Tag (opcional):");
    const location = prompt("Ubicación (opcional):");
    const criticality = prompt("Criticidad (Alta/Media/Baja):") || "Media";
    const status = prompt("Estatus (Operativo/Parado/Mantenimiento):") || "Operativo";
    const description = prompt("Descripción (opcional):");
    const payload = { name, sap_number:sap, tag, location, criticality, status, description };
    const r = await fetch('/api/equipment', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)});
    if (r.ok) renderList(await fetchEquipment());
    else alert('Error al crear');
  });
}
window.addEventListener('load', initial);
