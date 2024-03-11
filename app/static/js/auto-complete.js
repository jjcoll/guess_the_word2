const cwButton = document.querySelector('.cw-container')
const resultBox = document.querySelector('.result-box')
const searchBox = document.querySelector('.search-box')
const inputBox = document.querySelector('#search-wordlist')
const searchBtn = document.querySelector('.btn-wordlist-search')

let wordLists = []


// when click on change wordlist button
cwButton.addEventListener('click', (e) => {
    searchBox.classList.remove('d-none')
    // put focus on input box
    inputBox.focus()


    //get word list
    fetch('/get-wordlists')
        .then(response => response.json())
        .then(data => {
            wordLists = data
            display(wordLists.filter(wordList => wordList.featured === true), true);
        })
        .catch(error => console.error('Error:', error));


})

// close the search box when clicking 'x'
searchBtn.addEventListener('click', (e) => {
    resultBox.innerHTML = ''
    inputBox.value = ''
    searchBox.classList.add('d-none')
})

inputBox.onkeyup = () => {
    let result = [];
    let input = inputBox.value

    if (input.length) {
        result = wordLists.filter((wordlist) => {
            return wordlist.name.toLowerCase().includes(input);
        });

        if (result.length) {
            display(result, false)
        }
    } else {
        display(wordLists.filter(wordList => wordList.featured === true), true);
    }

}


const display = (result, featured) => {
    const content = result.map((wordlist) => {
        if (featured) {
            return `<li onclick=selectInput(this) value=${wordlist.file}><span>featured</span>&nbsp;&nbsp;&nbsp;${wordlist.name}</li>`
        } else {
            return `<li onclick=selectInput(this) value=${wordlist.file}>${wordlist.name}</li>`
        }
    });
    resultBox.innerHTML = "<ul>" + content.join('') + "</ul>"
}

const selectInput = (list) => {
    const wordlist = list.getAttribute('value')
    resultBox.innerHTML = ''

    // hide form
    searchBox.classList.add('d-none')
    fetch('/post-wordlist', {

        "method": "POST",
        "headers": { 'Content-type': 'application/json', 'X-CSRFToken': csrfToken },
        "body": JSON.stringify({
            "wordlist": wordlist
        })
    }).then(response => response.json()).then(data => {

        updateDisplay(data.updatedWord, data.updateLives, data.lives, data.won)
        const result = list.innerText.replace(/featured/g, '');
        document.querySelector('.show-wordlist').innerText = result

    }).catch(err => {
        console.log("Error:", err)
    })
}