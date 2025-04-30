const API_URL = 'https://twoj-backend.onrender.com/league'; // <- Podmień to później

async function fetchLeagueData() {
    const res = await fetch(API_URL);
    const data = await res.json();

    const tableBody = document.querySelector("#league-table tbody");
    tableBody.innerHTML = "";

    data.teams.forEach(([team, stats], index) => {
        const row = `
        <tr>
            <td>${index + 1}</td>
            <td>${team}</td>
            <td>${stats.Mecze}</td>
            <td>${stats.Punkty}</td>
            <td>${stats.Zwycięstwa}</td>
            <td>${stats.Remisy}</td>
            <td>${stats.Porażki}</td>
            <td>${stats["Bramki zdobyte"]}</td>
            <td>${stats["Bramki stracone"]}</td>
            <td>${stats.Bilans}</td>
        </tr>`;
        tableBody.innerHTML += row;
    });

    const scheduleBody = document.querySelector("#schedule-table tbody");
    scheduleBody.innerHTML = "";
    data.schedule.forEach(match => {
        scheduleBody.innerHTML += `
        <tr>
            <td>${match.Gospodarz}</td>
            <td>${match.Gość}</td>
            <td>${match.Wynik}</td>
        </tr>`;
    });
}

// Automatyczne odświeżanie co 10 sekund
setInterval(fetchLeagueData, 10000);
fetchLeagueData();
