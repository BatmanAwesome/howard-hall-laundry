const message = document.getElementById('update-status');
let hasSnapshot = false;

function machineCard(machine) {
    const isWasher = String(machine.type || '').toLowerCase() === 'washer';
    const offline = [machine.mode, machine.notAvailableReason]
        .some(value => String(value || '').toLowerCase() === 'offline');
    const available = machine.available === true && !offline;
    const remaining = Number(machine.timeRemaining);
    const statusText = offline ? 'Offline' : available ? 'Available'
        : Number.isFinite(remaining) && remaining > 0 ? `${remaining} mins left` : 'Busy';
    const item = document.createElement('div');
    item.className = 'machine-item';
    item.innerHTML = `
        <div class="card machine-card shadow-sm h-100 ${offline ? 'status-offline' : available ? 'status-free' : 'status-busy'}">
            <div class="card-body">
                <span class="badge ${isWasher ? 'badge-washer' : 'badge-dryer'} mb-2"></span>
                <h5 class="card-title"></h5>
                <p class="card-text"><strong></strong></p>
            </div>
        </div>`;
    item.querySelector('.badge').textContent = isWasher ? 'WASHER' : 'DRYER';
    item.querySelector('.card-title').textContent = `#${machine.stickerNumber ?? '???'}`;
    item.querySelector('strong').textContent = statusText;
    return item;
}

function renderGroup(data, type, containerId, countId) {
    const machines = data.filter(machine => String(machine.type || '').toLowerCase() === type);
    const container = document.getElementById(containerId);
    const scrollLeft = container.scrollLeft;
    container.replaceChildren(...machines.map(machineCard));
    container.scrollLeft = scrollLeft;
    if (!machines.length) {
        const empty = document.createElement('p');
        empty.className = 'p-3 text-muted';
        empty.textContent = `No ${containerId} reported.`;
        container.append(empty);
    }
    const free = machines.filter(machine => machine.available === true &&
        ![machine.mode, machine.notAvailableReason].some(value => String(value || '').toLowerCase() === 'offline')).length;
    document.getElementById(countId).textContent = `${free}/${machines.length} free`;
}

async function updateDashboard() {
    try {
        const response = await fetch('/api/status', {signal: AbortSignal.timeout(15000)});
        if (!response.ok) throw new Error('Status request failed');
        const data = await response.json();
        if (!Array.isArray(data) || data.some(machine => !machine || typeof machine !== 'object' || Array.isArray(machine))) {
            throw new Error('Invalid machine data');
        }
        document.getElementById('dashboard').hidden = false;
        renderGroup(data, 'washer', 'washers', 'washerCount');
        renderGroup(data, 'dryer', 'dryers', 'dryerCount');
        hasSnapshot = true;
        message.textContent = `Last checked: ${new Date().toLocaleTimeString()}`;
        message.classList.remove('text-danger');
    } catch (error) {
        message.textContent = hasSnapshot
            ? 'Unable to refresh. Displayed statuses may be out of date. Retrying automatically.'
            : 'Unable to load laundry status. Retrying automatically.';
        message.classList.add('text-danger');
    } finally {
        document.getElementById('loading').hidden = true;
        setTimeout(updateDashboard, 30000);
    }
}

document.addEventListener('wheel', event => {
    const strip = event.target.closest?.('.machine-strip');
    if (!strip || strip.scrollWidth <= strip.clientWidth) return;
    const delta = event.deltaY || event.deltaX;
    if (!delta) return;
    event.preventDefault();
    strip.scrollLeft += delta;
}, {passive: false});

updateDashboard();
