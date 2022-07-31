## Inspiration
I am a big fan of Pokemon and bird watching. I wanted to combine both my favorite things so I built BirdDex which is similar to Pokédex in the sense that it catalogues and provides information regarding bird species. Also whenever I go bird watching I would like a device like Pokédex which would catalogue and provide the information of the birds I capture (on my camera) and BirdDex does the exact same thing!

## What it does
When uploaded a picture it identifies the species of the bird in the picture, then it displays the picture, the common name, the scientific name, and the description of the species. You can play the sound of the bird by clicking on 'Play Sound', read the description by clicking on 'Read Description' and shuffle through all the birds with the help of up and down toggle buttons on the BirdDex.

## How we built it
1. The species of the bird is identified with the help of the bird species classification machine learning model trained by me. It can identify up to 400 species of birds when provided the photo of the bird.
2. The description is gathered from the summary of the wikipedia page of the bird species.
3. The sound is gather from xeno-canto API.
4. The scientific name is gotten by parsing the CSV file matching the common name with the scientific name.
5. The UI is created with the help of HTML, CSS and JavaScript and the backend is built in Flask.

## Challenges we ran into
1. Developing the bird species image classification model.

## Accomplishments that we're proud of
1. Was successfully able to train a bird species image classification model.
2. I was able to achieve the Pokédex UI. 

## What we learned
1. How to train an image classification model.
2. Build a complex UI using HTML and CSS.

## What's next for Bird Dex
1. Improving the machine learning model and providing support for more species of birds.
2. Adding ability to store multiple pictures of the species.
