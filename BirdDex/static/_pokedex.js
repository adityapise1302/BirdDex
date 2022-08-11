var index = 0;
var total_birds = 0;

/* This function configures the data on the pokedex interface. It sets the picture, bird index number, the name, the
 * description of the bird, the sound url, and the latin name of the bird on the pokedex interface.
 *
 * Parameter: bird_index - it is an integer suggesting the index of the bird which is to be displayed on the pokedex
 *                         interface.
 * Return: Null
 */
function setDataOnWindow(bird_index){
    fetch("http://127.0.0.1:8000/get_bird_data").then(function (response){
        return response.json();
    }).then(function (obj){
        console.log(obj)
        total_birds = Object.keys(obj).length;
        index = bird_index;
        document.getElementById("picture").src = obj[index.toString()]["img_url"];
        document.getElementById("number-bird").innerHTML = index.toString();
        document.getElementById("name-screen").innerHTML = obj[index.toString()]["name"];
        document.getElementById("screen-description").innerHTML = obj[index.toString()]["description"];
        document.getElementById("extra-info-screen-1").innerHTML = obj[index.toString()]["latin_name"];
        document.getElementById("extra-info-screen-2").setAttribute('onclick', 'playBirdSound("' + obj[index.toString()]["sound_url"] + '")');
    }).catch(function (error){
        console.error(error);
    });
}

/* This function submits the form which sends the photo of the uploaded bird to the backend Flask server.
 *
 * Parameter: Null
 * Return: Null
 */
function submit_form(){
    const form = document.getElementById("upload_photo");
    form.submit();
    setDataOnWindow(total_birds + 1);
}

/* This function reads the bird description in the description section of the pokedex.
 *
 * Parameter: Null
 * Return: Null
 */
function readDescription(){
    let speech = new SpeechSynthesisUtterance();
    speech.text = document.getElementById("screen-description").innerHTML;
    console.log(document.getElementById("screen-description").innerHTML);
    window.speechSynthesis.speak(speech);
}

/* This function stops the reading of the description.
 *
 * Parameter: Null
 * Return: Null
 */
function stopReading(){
    window.speechSynthesis.cancel();
}

/* This function plays the sound of the bird when url of the bird sound is provided.
 *
 * Parameter: url - it is a string suggesting the url of the bird sound to be played.
 * Return: Null
 */
function playBirdSound(url){
    new Audio(url).play();
}

/* This function executes when the up toggle button is clicked on the pokedex interface. It
 * shows the data of the bird whose index is one less than the bird present on the screen.
 * If the bird's index present on the screen is 1 then it shows the data of the bird last in
 * the database.
 *
 * Parameter: Null
 * Return: Null
 */
function clickUp(){
    if(index > 1){
        index = index - 1;
    } else{
        index = total_birds;
    }
    setDataOnWindow(index);
}

/* This function executes when the down toggle button is clicked on the pokedex interface. It
 * shows the data of the bird whose index is one more than the bird present on the screen.
 * If the bird's index present on the screen is the last index then it shows the data of the bird
 * whose index is 1.
 */
function clickBottom(){
    if(index < total_birds){
        index = index + 1;
    }else{
        index = 1;
    }
    setDataOnWindow(index);
}

setDataOnWindow(1);