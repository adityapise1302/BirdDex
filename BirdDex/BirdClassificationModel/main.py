import tensorflow as tf
import numpy as np
import pathlib
from tensorflow.keras import layers


def train_model():
    batch_size = 32
    img_height = 180
    img_width = 180
    data_dir = "./train/"
    data_dir = pathlib.Path(data_dir)

    train_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size
    )

    class_names = train_ds.class_names

    val_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size
    )

    AUTOTUNE = tf.data.AUTOTUNE

    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    normalization_layer = tf.keras.layers.Rescaling(1. / 255)

    normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
    image_batch, labels_batch = next(iter(normalized_ds))

    with tf.device('/cpu:0'):
        data_augmentation = tf.keras.Sequential(
            [
                layers.RandomFlip("horizontal",
                                  input_shape=(img_height,
                                               img_width,
                                               3)),
                layers.RandomRotation(0.1),
                layers.RandomZoom(0.1),
            ]
        )

    num_classes = len(class_names)

    model = tf.keras.Sequential([
        data_augmentation,
        layers.Rescaling(1. / 255),
        layers.Conv2D(16, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Dropout(0.2),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes)
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    model.build()
    model.summary()
    epochs = 15
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs
    )
    model.save("saved_model/bird_classification")


def predict_bird_species(img_path: str) -> str:
    img_height = 180
    img_width = 180
    model = tf.keras.models.load_model('/Users/adityapise/HackathonProjects/BirdDex/BirdDex/BirdClassificationModel'
                                       '/saved_model/bird_classification')
    class_names = ['ABBOTTS BABBLER', 'ABBOTTS BOOBY', 'ABYSSINIAN GROUND HORNBILL', 'AFRICAN CROWNED CRANE',
                   'AFRICAN EMERALD CUCKOO', 'AFRICAN FIREFINCH', 'AFRICAN OYSTER CATCHER', 'ALBATROSS',
                   'ALBERTS TOWHEE',
                   'ALEXANDRINE PARAKEET', 'ALPINE CHOUGH', 'ALTAMIRA YELLOWTHROAT', 'AMERICAN AVOCET',
                   'AMERICAN BITTERN',
                   'AMERICAN COOT', 'AMERICAN GOLDFINCH', 'AMERICAN KESTREL', 'AMERICAN PIPIT', 'AMERICAN REDSTART',
                   'AMETHYST WOODSTAR', 'ANDEAN GOOSE', 'ANDEAN LAPWING', 'ANDEAN SISKIN', 'ANHINGA', 'ANIANIAU',
                   'ANNAS HUMMINGBIRD', 'ANTBIRD', 'ANTILLEAN EUPHONIA', 'APAPANE', 'APOSTLEBIRD', 'ARARIPE MANAKIN',
                   'ASHY THRUSHBIRD', 'ASIAN CRESTED IBIS', 'AVADAVAT', 'AZURE JAY', 'AZURE TANAGER', 'AZURE TIT',
                   'BAIKAL TEAL', 'BALD EAGLE', 'BALD IBIS', 'BALI STARLING', 'BALTIMORE ORIOLE', 'BANANAQUIT',
                   'BAND TAILED GUAN', 'BANDED BROADBILL', 'BANDED PITA', 'BANDED STILT', 'BAR-TAILED GODWIT',
                   'BARN OWL',
                   'BARN SWALLOW', 'BARRED PUFFBIRD', 'BARROWS GOLDENEYE', 'BAY-BREASTED WARBLER', 'BEARDED BARBET',
                   'BEARDED BELLBIRD', 'BEARDED REEDLING', 'BELTED KINGFISHER', 'BIRD OF PARADISE',
                   'BLACK & YELLOW  BROADBILL', 'BLACK BAZA', 'BLACK COCKATO', 'BLACK FRANCOLIN', 'BLACK SKIMMER',
                   'BLACK SWAN', 'BLACK TAIL CRAKE', 'BLACK THROATED BUSHTIT', 'BLACK THROATED WARBLER',
                   'BLACK VULTURE',
                   'BLACK-CAPPED CHICKADEE', 'BLACK-NECKED GREBE', 'BLACK-THROATED SPARROW', 'BLACKBURNIAM WARBLER',
                   'BLONDE CRESTED WOODPECKER', 'BLUE COAU', 'BLUE GROUSE', 'BLUE HERON', 'BLUE THROATED TOUCANET',
                   'BOBOLINK', 'BORNEAN BRISTLEHEAD', 'BORNEAN LEAFBIRD', 'BORNEAN PHEASANT', 'BRANDT CORMARANT',
                   'BROWN CREPPER', 'BROWN NOODY', 'BROWN THRASHER', 'BULWERS PHEASANT', 'BUSH TURKEY', 'CACTUS WREN',
                   'CALIFORNIA CONDOR', 'CALIFORNIA GULL', 'CALIFORNIA QUAIL', 'CANARY', 'CAPE GLOSSY STARLING',
                   'CAPE LONGCLAW', 'CAPE MAY WARBLER', 'CAPE ROCK THRUSH', 'CAPPED HERON', 'CAPUCHINBIRD',
                   'CARMINE BEE-EATER', 'CASPIAN TERN', 'CASSOWARY', 'CEDAR WAXWING', 'CERULEAN WARBLER',
                   'CHARA DE COLLAR',
                   'CHATTERING LORY', 'CHESTNET BELLIED EUPHONIA', 'CHINESE BAMBOO PARTRIDGE', 'CHINESE POND HERON',
                   'CHIPPING SPARROW', 'CHUCAO TAPACULO', 'CHUKAR PARTRIDGE', 'CINNAMON ATTILA', 'CINNAMON FLYCATCHER',
                   'CINNAMON TEAL', 'CLARKS NUTCRACKER', 'COCK OF THE  ROCK', 'COCKATOO', 'COLLARED ARACARI',
                   'COMMON FIRECREST', 'COMMON GRACKLE', 'COMMON HOUSE MARTIN', 'COMMON IORA', 'COMMON LOON',
                   'COMMON POORWILL', 'COMMON STARLING', 'COPPERY TAILED COUCAL', 'CRAB PLOVER', 'CRANE HAWK',
                   'CREAM COLORED WOODPECKER', 'CRESTED AUKLET', 'CRESTED CARACARA', 'CRESTED COUA', 'CRESTED FIREBACK',
                   'CRESTED KINGFISHER', 'CRESTED NUTHATCH', 'CRESTED OROPENDOLA', 'CRESTED SHRIKETIT', 'CRIMSON CHAT',
                   'CRIMSON SUNBIRD', 'CROW', 'CROWNED PIGEON', 'CUBAN TODY', 'CUBAN TROGON', 'CURL CRESTED ARACURI',
                   'D-ARNAUDS BARBET', 'DARK EYED JUNCO', 'DEMOISELLE CRANE', 'DOUBLE BARRED FINCH',
                   'DOUBLE BRESTED CORMARANT', 'DOUBLE EYED FIG PARROT', 'DOWNY WOODPECKER', 'DUSKY LORY', 'EARED PITA',
                   'EASTERN BLUEBIRD', 'EASTERN GOLDEN WEAVER', 'EASTERN MEADOWLARK', 'EASTERN ROSELLA',
                   'EASTERN TOWEE',
                   'ELEGANT TROGON', 'ELLIOTS  PHEASANT', 'EMERALD TANAGER', 'EMPEROR PENGUIN', 'EMU', 'ENGGANO MYNA',
                   'EURASIAN GOLDEN ORIOLE', 'EURASIAN MAGPIE', 'EUROPEAN GOLDFINCH', 'EUROPEAN TURTLE DOVE',
                   'EVENING GROSBEAK', 'FAIRY BLUEBIRD', 'FAIRY TERN', 'FIORDLAND PENGUIN', 'FIRE TAILLED MYZORNIS',
                   'FLAME BOWERBIRD', 'FLAME TANAGER', 'FLAMINGO', 'FRIGATE', 'GAMBELS QUAIL', 'GANG GANG COCKATOO',
                   'GILA WOODPECKER', 'GILDED FLICKER', 'GLOSSY IBIS', 'GO AWAY BIRD', 'GOLD WING WARBLER',
                   'GOLDEN CHEEKED WARBLER', 'GOLDEN CHLOROPHONIA', 'GOLDEN EAGLE', 'GOLDEN PHEASANT', 'GOLDEN PIPIT',
                   'GOULDIAN FINCH', 'GRAY CATBIRD', 'GRAY KINGBIRD', 'GRAY PARTRIDGE', 'GREAT GRAY OWL',
                   'GREAT JACAMAR',
                   'GREAT KISKADEE', 'GREAT POTOO', 'GREATOR SAGE GROUSE', 'GREEN BROADBILL', 'GREEN JAY',
                   'GREEN MAGPIE',
                   'GREY PLOVER', 'GROVED BILLED ANI', 'GUINEA TURACO', 'GUINEAFOWL', 'GURNEYS PITTA', 'GYRFALCON',
                   'HAMMERKOP', 'HARLEQUIN DUCK', 'HARLEQUIN QUAIL', 'HARPY EAGLE', 'HAWAIIAN GOOSE', 'HAWFINCH',
                   'HELMET VANGA', 'HEPATIC TANAGER', 'HIMALAYAN BLUETAIL', 'HIMALAYAN MONAL', 'HOATZIN',
                   'HOODED MERGANSER', 'HOOPOES', 'HORNBILL', 'HORNED GUAN', 'HORNED LARK', 'HORNED SUNGEM',
                   'HOUSE FINCH',
                   'HOUSE SPARROW', 'HYACINTH MACAW', 'IBERIAN MAGPIE', 'IBISBILL', 'IMPERIAL SHAQ', 'INCA TERN',
                   'INDIAN BUSTARD', 'INDIAN PITTA', 'INDIAN ROLLER', 'INDIGO BUNTING', 'INLAND DOTTEREL', 'IVORY GULL',
                   'IWI', 'JABIRU', 'JACK SNIPE', 'JANDAYA PARAKEET', 'JAPANESE ROBIN', 'JAVA SPARROW', 'KAGU',
                   'KAKAPO',
                   'KILLDEAR', 'KING VULTURE', 'KIWI', 'KOOKABURRA', 'LARK BUNTING', 'LAZULI BUNTING',
                   'LESSER ADJUTANT',
                   'LILAC ROLLER', 'LITTLE AUK', 'LONG-EARED OWL', 'MAGPIE GOOSE', 'MALABAR HORNBILL',
                   'MALACHITE KINGFISHER', 'MALAGASY WHITE EYE', 'MALEO', 'MALLARD DUCK', 'MANDRIN DUCK',
                   'MANGROVE CUCKOO',
                   'MARABOU STORK', 'MASKED BOOBY', 'MASKED LAPWING', 'MIKADO  PHEASANT', 'MOURNING DOVE', 'MYNA',
                   'NICOBAR PIGEON', 'NOISY FRIARBIRD', 'NORTHERN CARDINAL', 'NORTHERN FLICKER', 'NORTHERN FULMAR',
                   'NORTHERN GANNET', 'NORTHERN GOSHAWK', 'NORTHERN JACANA', 'NORTHERN MOCKINGBIRD', 'NORTHERN PARULA',
                   'NORTHERN RED BISHOP', 'NORTHERN SHOVELER', 'OCELLATED TURKEY', 'OKINAWA RAIL',
                   'ORANGE BRESTED BUNTING',
                   'ORIENTAL BAY OWL', 'OSPREY', 'OSTRICH', 'OVENBIRD', 'OYSTER CATCHER', 'PAINTED BUNTING', 'PALILA',
                   'PARADISE TANAGER', 'PARAKETT  AKULET', 'PARUS MAJOR', 'PATAGONIAN SIERRA FINCH', 'PEACOCK',
                   'PELICAN',
                   'PEREGRINE FALCON', 'PHILIPPINE EAGLE', 'PINK ROBIN', 'POMARINE JAEGER', 'PUFFIN', 'PURPLE FINCH',
                   'PURPLE GALLINULE', 'PURPLE MARTIN', 'PURPLE SWAMPHEN', 'PYGMY KINGFISHER', 'QUETZAL',
                   'RAINBOW LORIKEET', 'RAZORBILL', 'RED BEARDED BEE EATER', 'RED BELLIED PITTA', 'RED BROWED FINCH',
                   'RED FACED CORMORANT', 'RED FACED WARBLER', 'RED FODY', 'RED HEADED DUCK', 'RED HEADED WOODPECKER',
                   'RED HONEY CREEPER', 'RED NAPED TROGON', 'RED TAILED HAWK', 'RED TAILED THRUSH',
                   'RED WINGED BLACKBIRD',
                   'RED WISKERED BULBUL', 'REGENT BOWERBIRD', 'RING-NECKED PHEASANT', 'ROADRUNNER', 'ROBIN',
                   'ROCK DOVE',
                   'ROSY FACED LOVEBIRD', 'ROUGH LEG BUZZARD', 'ROYAL FLYCATCHER', 'RUBY THROATED HUMMINGBIRD',
                   'RUDY KINGFISHER', 'RUFOUS KINGFISHER', 'RUFUOS MOTMOT', 'SAMATRAN THRUSH', 'SAND MARTIN',
                   'SANDHILL CRANE', 'SATYR TRAGOPAN', 'SCARLET CROWNED FRUIT DOVE', 'SCARLET IBIS', 'SCARLET MACAW',
                   'SCARLET TANAGER', 'SHOEBILL', 'SHORT BILLED DOWITCHER', 'SMITHS LONGSPUR', 'SNOWY EGRET',
                   'SNOWY OWL',
                   'SORA', 'SPANGLED COTINGA', 'SPLENDID WREN', 'SPOON BILED SANDPIPER', 'SPOONBILL', 'SPOTTED CATBIRD',
                   'SRI LANKA BLUE MAGPIE', 'STEAMER DUCK', 'STORK BILLED KINGFISHER', 'STRAWBERRY FINCH',
                   'STRIPED OWL',
                   'STRIPPED MANAKIN', 'STRIPPED SWALLOW', 'SUPERB STARLING', 'SWINHOES PHEASANT', 'TAILORBIRD',
                   'TAIWAN MAGPIE', 'TAKAHE', 'TASMANIAN HEN', 'TEAL DUCK', 'TIT MOUSE', 'TOUCHAN', 'TOWNSENDS WARBLER',
                   'TREE SWALLOW', 'TROPICAL KINGBIRD', 'TRUMPTER SWAN', 'TURKEY VULTURE', 'TURQUOISE MOTMOT',
                   'UMBRELLA BIRD', 'VARIED THRUSH', 'VENEZUELIAN TROUPIAL', 'VERMILION FLYCATHER',
                   'VICTORIA CROWNED PIGEON', 'VIOLET GREEN SWALLOW', 'VIOLET TURACO', 'VULTURINE GUINEAFOWL',
                   'WALL CREAPER', 'WATTLED CURASSOW', 'WATTLED LAPWING', 'WHIMBREL', 'WHITE BROWED CRAKE',
                   'WHITE CHEEKED TURACO', 'WHITE NECKED RAVEN', 'WHITE TAILED TROPIC', 'WHITE THROATED BEE EATER',
                   'WILD TURKEY', 'WILSONS BIRD OF PARADISE', 'WOOD DUCK', 'YELLOW BELLIED FLOWERPECKER',
                   'YELLOW CACIQUE',
                   'YELLOW HEADED BLACKBIRD']

    img = tf.keras.utils.load_img(
        img_path, target_size=(img_height, img_width)
    )

    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    return class_names[np.argmax(score)]
