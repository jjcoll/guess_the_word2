const alertInfo1 = `     <div class="alert alert-info alert-dismissible ">
        Survival mode lets you play continuously until you run out of lives, and your score will be saved!
        <button type="button" class="btn-close" aria-label="Close" data-bs-dismiss="alert"></button>
    </div>`

const alertInfo2 = `     <div class="alert alert-danger alert-dismissible ">
    You can't switch in the middle of a game!
        <button type="button" class="btn-close" aria-label="Close" data-bs-dismiss="alert"></button>
    </div>`


document.querySelector('#SurvivalModeExplain').addEventListener('click', (e) => {
    document.querySelector('.game-container').insertAdjacentHTML('afterbegin', alertInfo1)
})

document.querySelector('.trigger-survival').addEventListener('click', (e) => {
    const data = {
        'survival': e.target.checked
    }

    fetch('/trigger-survival', {
        "method": "POST",
        "headers": { 'Content-type': 'application/json', 'X-CSRFToken': csrfToken },
        "body": JSON.stringify(data)
    }).then(response => response.json())
        .then(data => {

            console.log(data.score)
            if (!data.started && data.score == 0) {
                // trigger switch
                if (data.survival) {
                    document.querySelector('.score').classList.remove('d-none')
                } else {
                    document.querySelector('.score').classList.add('d-none')
                }

            } else if (data.started || data.score > 0) {
                document.querySelector('.game-container').insertAdjacentHTML('afterbegin', alertInfo2)

                // do not change switch
                if (document.querySelector('.trigger-survival').checked) {
                    document.querySelector('.trigger-survival').checked = false
                } else {
                    document.querySelector('.trigger-survival').checked = true
                }
            } else {
                location.reload()
            }
        })
        .catch(error => {
            console.log(error)
        })
})


