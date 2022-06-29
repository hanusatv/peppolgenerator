function setRoot() {
    path = document.getElementById('rootdir').value
    fetch('/setroot', {
        method: 'POST',
        headers: {
            rootdir: path
        }
    }).then(window.location.reload())
}