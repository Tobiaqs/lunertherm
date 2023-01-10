window.addEventListener('load', () => {
    const lastUpdated = document.getElementById('last-updated')
    const currentTemp = document.getElementById('current-temp')
    const targetTemp = document.getElementById('target-temp')
    const heating = document.getElementById('heating')
    const relay = document.getElementById('relay')

    const reload = () => {
        fetch('/state').then((response) => response.json()).then((response) => {
            currentTemp.innerText = (Math.round(response.current_temp / 100) / 10) + ' °C'
            targetTemp.innerText = (Math.round(response.target_temp / 100) / 10) + ' °C'
            heating.innerText = response.heating ? 'ON' : 'OFF'
            relay.innerText = response.relay ? 'ON' : 'OFF'
            if (response.updated) {
                const date = new Date(response.updated + 'Z')
                lastUpdated.innerText = date.toLocaleString('nl-NL')
            } else {
                lastUpdated.innerText = 'never'
            }
        })
    }

    reload()

    setInterval(reload, 5000)

    document.getElementById('btn-update').addEventListener('click', () => {
        location.href = '/update'
    })
});
