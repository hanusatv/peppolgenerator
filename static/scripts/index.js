function test(e) {
    let modal = new bootstrap.Modal(document.getElementById('staticBackdrop'))
    modal.show()
    setTimeout(function () {
        modal.hide()
    },
        2000)
}

async function createfiles(e) {
    let card = e.closest("#card")
    let subdir = card.querySelector('#subdir').innerText
    let modal = new bootstrap.Modal(document.getElementById('staticBackdrop'))
    modal.show()
    setTimeout(() => {
        fetch('/createfiles', {
            method: 'POST',
            headers: {
                'subdir': subdir
            }
        }).then(res => {
            if (!res.ok) {
                alert('Something went wrong. Try restaring the service')
            }
            modal.hide()
            window.location.reload()
        })
    }, 1000)
}