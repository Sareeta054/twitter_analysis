/**
 * Author: Bipin Oli
 */

const fs = require("fs")
const path = require("path")
const url = require("url")
const https = require("https")
const Hippo = require("wordhippo")
const YAML = require("yaml")

// console.log(Hippo)

// steps
// 1. read aspect config file
// 2. fetch the related words
// 3. generate sentences containing the aspect 
// 4. generate sentences containing related words of aspect
// 5. save sentences into json file along with their aspect
// 6. the json file will be read by the classifier to classify the sentences
// 7. classified sentences along with aspect will be used to train the BERT model


// read aspects specified in config file
function readAspects() {
    console.log("------ reading aspects from config file -----");
    const configPath = path.join(__dirname,'..', 'config', 'aspectConfigs.yml');
    const aspectConfigFile = fs.readFileSync(configPath, 'utf8');
    return YAML.parse(aspectConfigFile)['aspects'];
}

// fetch related words of aspects
function fetchRelatedWordsOfAspects(aspects) {
    console.log("--- fetching related words of aspects read from the config file ----");
    return new Promise(function(resolve, reject) {
        let promisesList = [];
        for (let i=0; i<aspects.length; i++) {
            promisesList.push(fetchRelatedWords(aspects[i]));
        }        
        Promise.all(promisesList)
            .then(result => {
                resolve(result);
            })
            .catch(err => reject(err));
    });
}

// generate sentences containing the aspect or related words
function genSentences(tempData = undefined) {
    console.log("---- generating sentences ------");
    return new Promise(function (resolve, reject) {
        const aspects = readAspects();
        fetchRelatedWordsOfAspects(aspects)
            .then(data => {
                // console.log(data);
                /* 
                    data = [ {aspect1: [ .. related words ..]}, {aspect2: [ .. related words ..]}, ... ]
                */
                let promisesList = [];
                for (let i=0; i<data.length; i++) {
                    let aspect = Object.keys(data[i])[0];
                    // input words = [ aspect, .. related words of aspect ...]
                    promisesList.push(genSentencesFromWords([ aspect, ...data[i][aspect] ], tempData));
                }
                Promise.all(promisesList)
                    .then(result => {
                        // result is the list of list of sentences
                        let retval = []; // in json style 
                        for (let i=0; i<data.length; i++) {
                            let aspect = Object.keys(data[i])[0];
                            let obj = {};
                            obj[aspect] = result[i];
                            retval.push(obj);
                        }
                        resolve(retval);
                    })
                    .catch(err => {
                        reject(err);
                    });
            })
            .catch(err => reject(err));
    });
}

// generate and save sentences into a json file
function generateSentencesIntoJsonFile(tempData = undefined) {
    console.log("--- generating sentences and saving into a json file --- ");

    return new Promise(function (resolve, reject) {
        genSentences(tempData)
            .then(result => {
                let jsonResult = JSON.stringify(result);
                fs.writeFileSync('generatedSentences.json', jsonResult, 'utf8');
                resolve(true);
            })
            .catch(err => {
                console.log("\n\n\ntempdata: ", tempData);
                if (tempData && Object.keys(tempData).length > 0)
                    saveTempFile(tempData);
                console.log("\n\n--- ERROR: " + err.message + " -------\n\n");
                reject("unfinished sentence generation");
            });
    });
}

// generate list of sentences containing at least one word from the given words
function genSentencesFromWords(words, tempData = undefined) {
    console.log("\n\n-++++ generating sentences from words --+++");
    // console.log("generating sentences from : ", words);

    return new Promise(function (resolve, reject) {

        waitFor(1000);
        
        let promisesList = [];
        for (let i=0; i<words.length; i++)
            promisesList.push(genSentencesFromWord(words[i], tempData));
        
        Promise.all(promisesList)
            .then(result => {
                // result = list of list of sentences
                // merge all lists into single list of sentences
                resolve(result.flat());
            })
            .catch(err => {
                // console.log("\n\n--- ERROR: " + err.message + " ---\n\n");
                reject(err);
            });
    });
}

// let wordCount = 0;

// generate sentences containing the given word
function genSentencesFromWord(word, tempData = undefined) {
    // console.log("---- generate sentences from word: " + word + " -----");
    return new Promise(function (resolve, reject) {

        // waitFor(2000);

        
        // before asking the server check if data is available in tempData
        if (tempData && word in tempData) {
            console.log("---- data found in tempdata ----");
            resolve(tempData[word]);
        }
        else {
            console.log("---- requesting hippo ----------");
            // encode word as a url parameter
            Hippo.sentences(encodeURI(word))
                .then(data => {
                    console.log("--++ generated sentences from word: " + word + " -----");
                    if (tempData) {
                        tempData[word] = data;
                        // console.log("tempdata: ", tempData);
                        // wordCount += 1;
                    }
                    resolve(data);
                })
                .catch(err => {
                    // console.log("\n\n--- ERROR: " + err.message + " ---\n\n");
                    reject(err);
                });
            }
    });
}

// get temp file to store the obtained result
// so that there is not need to request that again
function readTempFile() {
    console.log("----- reading temp file -------");
    const tempPath = path.join(__dirname, "tempSentences.json");
    let tempFile = fs.readFileSync(tempPath);
    return JSON.parse(tempFile);
}

// save tempfile
function saveTempFile(tempData) {
    console.log("------ saving the temp file ----------");
    const tempPath = path.join(__dirname,"tempSentences.json");
    fs.writeFileSync(tempPath, JSON.stringify(tempData));
}

// fetch the related words 
function fetchRelatedWords(aspect) {
    console.log("-- fetching related words for " + aspect);
    return new Promise(function(resolve, reject) {
        let apiUrl = "https://relatedwords.org/api/related?term=" + url.parse(aspect).path;
        console.log("\n\n fetching from url: " + apiUrl + "\n\n");

        https.get(apiUrl, (resp) => {
            let data = "";

            // a chunk of data has been received
            resp.on("data", (chunk) => {
                data += chunk;
            });

            // whole data has been received
            resp.on("end", () => {
                // words come like this:
                // { word: 'holism', from: 'swiki', score: 0.9268965517241378 }
                // console.log(JSON.parse(data));  
                let retval = []; // list of words
                JSON.parse(data).forEach((wordObj) => {
                    retval.push(wordObj.word);
                }); 
                // console.log(retval);
                toReturn = {};
                toReturn[aspect] = retval;
                resolve(toReturn);
            });
        }).on("error", (err) => {
            console.log("\n\n--- ERROR: " + err.message + " -------\n\n");
            reject(err);
        });
    });
}


// repeatedly generate sentences into temp file
// until server stops returning error
async function generateAllSentences() {

    while(true) {
        let tempData = readTempFile();
        
        try {
            let fulfilledValue = await generateSentencesIntoJsonFile(tempData);
            console.log(fulfilledValue);
            if (fulfilledValue)
                break;
        } catch(rejectedValue) {
            console.log("----- ", rejectedValue, " ---------");
        }

        waitFor(5000);        
    }

}

// synchronous wait function
function waitFor(milliSeconds = 5000) {
    let start = Date.now(),
    now = start;
    while (now - start < milliSeconds) 
       now = Date.now();
}



generateAllSentences();




// ------------------------- TESTING -------------------------------------

// genSentences();

// data = {name: "bipin", friends: ["rupesh", "atosh", "alekh", "alok", "sarita", "ejan", "aashish"]};
// saveTempFile(data);
// data = readTempFile();
// console.log(data);
// data['surname'] = "Oli";
// saveTempFile(data);


// fetchRelatedWordsOfAspects(["politics", "jobs", "immigration", "education", "health care", "jobs"])
//     .then(result => {
//         console.log(result);
//     });


// genSentencesFromWords(["happy", "sad"])
//     .then(result => console.log(result));


// genSentencesFromWord("health care")
//     .then(result => console.log(result));

// genSentencesFromWord("international standard industrial classification")
//     .then(result => console.log(result));

// genSentencesFromWord("health administration")
//     .then(result => console.log(result));

// Hippo.sentences("play")
//     .then(
//         (data) => {
//             console.log(data);
//         }
//     )
