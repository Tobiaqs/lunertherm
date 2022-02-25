window.addEventListener('load', () => {
    const targetTemp = document.getElementById('target-temp')
    const btnTargetTemp = document.getElementById('btn-target-temp')
    const relay = document.getElementById('relay')
    const btnRelay = document.getElementById('btn-relay')

    targetTemp.addEventListener('input', () => {
        btnTargetTemp.classList.remove('opacity-0')
    })

    relay.addEventListener('click', () => {
        btnRelay.classList.remove('opacity-0')
        if (relay.classList.contains('bg-gray-200')) {
            relay.classList.remove('bg-gray-200')
            relay.classList.add('bg-green-600')
            relay.children[0].classList.remove('translate-x-0')
            relay.children[0].classList.add('translate-x-5')
        } else {
            relay.classList.add('bg-gray-200')
            relay.classList.remove('bg-green-600')
            relay.children[0].classList.add('translate-x-0')
            relay.children[0].classList.remove('translate-x-5')
        }
    })

    btnTargetTemp.addEventListener('click', () => {
        const val = targetTemp.value.trim().replace(',', '.')
        const valFloat = parseFloat(val)
        if (isNaN(valFloat) || valFloat < 5 || valFloat > 30) {
            alert('Invalid temperature! Needs to be >= 5 and <= 30')
            return
        }
        if (confirm('Are you sure? Setting temperature to ' + valFloat)) {
            fetch('/send/temp', { method: 'POST', body: valFloat }).then((response) => response.text()).then((response) => {
                if (response === 'ok') {
                    alert('Great success')
                    location.href = '/'
                } else if (response === 'not ok') {
                    alert('Please wait one minute before sending another command')
                } else {
                    alert('An error occurred')
                }
            })
        }
    })

    btnRelay.addEventListener('click', () => {
        if (confirm('Are you sure?')) {
            const relayValue = relay.classList.contains('bg-green-600')
            fetch('/send/relay', { method: 'POST', body: relayValue ? '1' : '0' }).then((response) => response.text()).then((response) => {
                if (response === 'ok') {
                    alert('Great success')
                    location.href = '/'
                } else if (response === 'not ok') {
                    alert('Please wait one minute before sending another command')
                } else {
                    alert('An error occurred')
                }
            })
        }
    })

    document.getElementById('btn-request-update').addEventListener('click', () => {
        fetch('/request_update', { method: 'POST' }).then((response) => response.text()).then((response) => {
            if (response === 'ok') {
                alert('Update requested!')
                location.href = '/'
            } else {
                alert('Update was already requested less than 1 min ago!')
            }
        })
    })

    document.getElementById('btn-back').addEventListener('click', () => {
        location.href = '/'
    })

    fetch('/state').then((response) => response.json()).then((response) => {
        if (response.relay) {
            relay.click()
            btnRelay.classList.add('opacity-0')
        }
    })
});
