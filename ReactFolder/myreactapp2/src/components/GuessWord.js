import {useState} from 'react'
import './guessWord.css';
function hiddenWord(){
    let words  = ['hello', 'steal', 'happy','great', 
                    'sweet', 'sweat', 'death', 'break', 'ocean', 'grind', 
                    'bread', 'drink', 'torch', 'phone', 'plane', 'swing',
                    'blank', 'swing', 'blink', 'think', 'green', 'fling',
                    'nice', 'large', 'kind', 'grief', 'shallow', 'swallow',
                    'hunt', 'burnt', 'butter', 'live', 'love', 'laugh', 'play'

            ]
    // words = ['hello']
    const randIdx = Math.floor(Math.random() * words.length)
    return words[randIdx]
}



function compare(guess, randWord){
    console.log(guess, randWord)
    const coloring = new Array(guess.length).fill("B")
    //  count occurence of each character in randWord
    const charCount = {}
    for(let char of randWord){
        if(!charCount.hasOwnProperty(char)){
            charCount[char] = 1
        } else{
            charCount[char] += 1
        }
    }
    for(let idx = 0; idx < guess.length; idx++){
        let guessChar = guess[idx]
        let randChar =randWord[idx]
        let countable = charCount[guessChar] ? charCount[randChar] > 0 : false

        if (countable){
            if(guessChar === randChar){
                coloring[idx] = 'G'
                charCount[guessChar] -= 1
            }
        }
    }
    for(let idx = 0; idx < guess.length; idx++){
        let guessChar = guess[idx]
        let randChar =randWord[idx]

        let countable = charCount[guessChar] ? charCount[guessChar] > 0 : false
        if (countable){
            if(guessChar !== randChar ){
                coloring[idx] = 'Y'
                charCount[guessChar] -= 1
            }
        }
    }
    console.log(charCount)
    console.log(coloring)
    return coloring
}


export default function GuessWord(props){
    
    const [randWord, setRandWWord] = useState(hiddenWord())
    
    // Set trials 
    const [trialsLeft, setTrialsLeft]  = useState(randWord.length + 1)
    const [guess, setGuess] = useState(new Array(randWord.length).fill('*'))

    // Set colors to grey at first
    // Set Colors
    const [colors, setColors] = useState(new Array(randWord.length).fill('B'))
    // Set correct
    const [correct, setCorrect] = useState(false)

    function refresh(e){
        setRandWWord(hiddenWord())
        setTrialsLeft(randWord.length + 1)
        setGuess(new Array(randWord.length).fill('*'))
        setColors(new Array(randWord.length).fill('B'))
        setCorrect(false)
    }

    function setKey(e){
        const acceptedKeys = 'abcdefghijklmnopqrstuvwxyz'
        let keyVal = "*"
        
        if(acceptedKeys.includes(e.key)) {keyVal = e.key
        
            setGuess(prevGuess => {
                let newGuess = prevGuess.slice()
                newGuess[e.target.id] = keyVal
                return newGuess
            })
            console.log(guess)
            e.target.nextElementSibling.focus()
        }
    }

    function submitGuess(e){
        const guessedWord = guess.join("")
        const selected = compare(guessedWord, randWord)
        setColors(prevColors => selected)
        setTrialsLeft(prevVal => prevVal - 1)

        // Check if all Correct
        const correctGuess = selected.every(col => col === 'G')
        setCorrect(correctGuess)
        
    }

    const button = <button className='refresh' onClick={refresh}>Click to Refresh</button>

    const correctData = (<div>
            <li>Your guess {randWord} is correct. </li>
            <li>Trials Left: {trialsLeft}</li>
            {button}
    </div>)
    return  correct ? correctData: (<>
        <h1>Guess Word Trials left {trialsLeft}</h1>
        {
        trialsLeft > 0 ? <>
                
                    
                    <div className='colorMeaning'>
                        <span className='meaning G'>Means the right character is in the right place</span>
                        <span className='meaning Y'>Means the character is in the original word, but in the wrong place</span>
                        <span className='meaning B'>Means the character is not in the original word</span>
                    </div>

                    <div className='guesses'>
                        {
                            guess.map((char, id) => {
                                return <input key={id} id={id} className={`char ${colors[id]}`} value={char} onKeyDown={setKey}/>
                            })
                        }

                        <button onClick={submitGuess}>Check Guess</button>
                    </div>

        </> :  <p>Trials Exceeded. {button}</p>


}
    </>)
}
