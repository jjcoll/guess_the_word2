// document.querySelectorAll('.letter').forEach(letter => {
//     letter.addEventListener('click', (e) => {
//         // get pressed letter
//         pressed_letter = e.currentTarget.id

//         // change the class list to make the letter used
//         e.currentTarget.classList.replace('letter', 'letter-used')
//         console.log(pressed_letter)

//         // send POST request to server with letter

//         fetch('/guess', {
//             method: "POST",
//             headers: {
//                 'Content-type': 'application/json'
//             },
//             body: JSON.stringify({ letter: pressed_letter })
//         })
//             .then(response => {
//                 console.log(response)
//                 return response.json()
//             })
//             .then(data => {
//                 console.log(data)
//                 // update HTML based on servers response
//                 updateDisplay(data.updatedWord, data.updateLives, data.lives, data.won)
//             }).catch(error => console.log('Error: ', error))
//     })
// })



// const changeWordList = (wordslist) => {
//     document.querySelectorAll('.game-option').forEach(option => {
//         if (wordslist === option.value) {
//             option.setAttribute('selected', true)
//         }
//     })
// }


// const gameModeInput = document.querySelector('#inputGameSelect')
// gameModeInput.addEventListener('change', (e) => {
//     const file_name = e.target.value
//     fetch('/change-wordlist', {
//         method: "POST",
//         headers: {
//             'Content-type': 'application/json'
//         },
//         body: JSON.stringify({ wordsfile: file_name })
//     }).then(response => response.json()).then(data => {
//         updateDisplay(data.updatedWord, data.updateLives, data.lives, data.won)

//         console.log(data.wordsfile)
//         changeWordList(data.wordsfile)

//         // TODO: must reactivate the letters
//     }).catch(error => console.log('Error', error))
// })

const csrfToken = document.querySelector("meta[name='csrf-token']").getAttribute("content");


const updateDisplay = (updatedWord, updateLives, lives, won) => {
    document.querySelector('.display-word').textContent = updatedWord;
    if (updateLives) {
        const liveContainer = document.querySelector('.lives');
        const lastHeart = liveContainer.lastElementChild;
        if (lastHeart) {
            liveContainer.removeChild(lastHeart);
        }
    }
    if (lives === 0) {
        // Take the player to game over window
        window.location.href = '/game-over?outcome=lose'
    }
    if (won) {
        window.location.href = '/game-over?outcome=win'
    }

};

document.querySelectorAll('.letter').forEach(letter => {
    letter.addEventListener('click', e => {

        // disable change wordlist
        cwButton.classList.add('d-none')

        const letter = e.currentTarget.id

        e.currentTarget.classList.replace('letter', 'letter-used')


        const data = {
            'letter': letter
        }

        fetch('/guess', {
            "method": "POST",
            "headers": { 'Content-type': 'application/json', 'X-CSRFToken': csrfToken },
            "body": JSON.stringify(data)
        }).then(response => response.json())
            .then(data => {
                updateDisplay(data.updatedWord, data.updateLives, data.lives, data.won)
            })
            .catch(error => {
                console.log(error)
            })
    })
})


