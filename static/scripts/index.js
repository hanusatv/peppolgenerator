function copySubdir(e) {
    let myToast = new bootstrap.Toast(document.getElementById('copiedToClipboard'))
    let clipboardtext = e.previousElementSibling.value
    navigator.clipboard.writeText(clipboardtext);
    myToast.show()
    setTimeout(() => { myToast.hide() }, 5000)
}

async function createfiles(e) {
    let card = e.closest("#card")
    console.log(card)
    let subdir = card.querySelector('#subdir').value
    console.log(subdir)
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
                alert('Something went wrong. Check your settings and/or try restaring the service')
            }
            modal.hide()
            window.location.reload()
        })
    }, 1000)
}