var index = 0;
var total_birds = 0;

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

function submit_form(){
    const form = document.getElementById("upload_photo");
    form.submit();
    setDataOnWindow(total_birds + 1);
}

function readDescription(){
    let speech = new SpeechSynthesisUtterance();
    speech.text = document.getElementById("screen-description").innerHTML;
    console.log(document.getElementById("screen-description").innerHTML);
    window.speechSynthesis.speak(speech);
}

function stopReading(){
    window.speechSynthesis.cancel();
}

function playBirdSound(url){
    new Audio(url).play();
}

function clickUp(){
    if(index > 1){
        index = index - 1;
    } else{
        index = total_birds;
    }
    setDataOnWindow(index);
}

function clickBottom(){
    if(index < total_birds){
        index = index + 1;
    }else{
        index = 1;
    }
    setDataOnWindow(index);
}

setDataOnWindow(1);