What I did:

Got data from here: https://www.yme.gr/metafores/adeies-odigisis/theoritiki-exetasi-ypopsifion-odigon-meso-i-y-mstheyo/item/6996-egkatastasi-programmatos-testdrive

=> cabextract

=> replace exerbase as described above

=> mdb -> json: https://lytrax.io/blog/tools/access-converter

attempt to understand json layout:

[
    { // 0
        "name":"Answer",
        "columns":[
            {
                "name":"AQCod", // answer code?
                "type":"LONG",
                "size":4
            },
            {
                "name":"AAA",
                "type":"INT",
                "size":2
            },
            {
                "name":"ALect", // answer text
                "type":"TEXT",
                "size":510
            },
            {
                "name":"ACorr", // answer correct or not
                "type":"BOOLEAN",
                "size":1
            },
            {
                "name":"ASound", // who knows??? probably for viewing in a UI while debugging, since this is the same data in the other fields basically
                "type":"TEXT",
                "size":20
            }
        ],
        "data":[ ... ]
    },
    { // 1
        "name":"Kateg",
        "columns":[
            {
                "name":"KCod", // category code, only important thing here! probably corresponding to the ενότητες [here](https://www.drivepoint.gr/erotiseis/enotita/motosikleta), so I can safely (?) drop the last two (pretty sure the first (motorcycles) is needed).
                "type":"BYTE",
                "size":1
            },
            {
                "name":"KLect", // name of lecture
                "type":"TEXT",
                "size":100
            },
            {
                "name":"KTime", // idk, idc
                "type":"BYTE",
                "size":1
            },
            {
                "name":"KPict", // jpg name
                "type":"TEXT",
                "size":30
            }
        ],
        "data":[ ... ]
    }, 
    { // 2 
         "name":"Numbs", // this WILL drive me insane, so I AM skipping it!
        "columns":[
            {
                "name":"KCod",
                "type":"LONG",
                "size":4
            },
            {
                "name":"PCod",
                "type":"BYTE",
                "size":1
            },
            {
                "name":"Lect",
                "type":"TEXT",
                "size":100
            },
            {
                "name":"Numb",
                "type":"BYTE",
                "size":1
            }
        ],
        "data":[ ... ]
    }, 
    { // 3
        "name":"Quest",
        "columns":[
            {
                "name":"QCod", // this should correspond to the answer code
                "type":"LONG",
                "size":4
            },
            {
                "name":"QKateg", // codes from above, remember, drop 4 and 5 (maybe print a few during debugging to make sure they're unneeded?)
                "type":"BYTE",
                "size":1
            },
            {
                "name":"QPag", // I'm going to assume this means "page", referring to some book where all these questions come from. might find the probability distribution for this later to check if it's uniform.
                "type":"BYTE",
                "size":1
            },
            {
                "name":"QLang", // interested in 1, for Greek
                "type":"BYTE",
                "size":1
            },
            {
                "name":"QLect", // question text 
                "type":"TEXT",
                "size":510
            },
            {
                "name":"QPhoto", // jpg name
                "type":"TEXT",
                "size":100
            },
            {
                "name":"QSound", // I bet it matches the other sound above, still don't care
                "type":"TEXT",
                "size":20
            },
            {
                "name":"QBook", // different parts, like "motorway" or "visibility". would prefer if this was also machine readable, but as far as I can tell it isn't anywhere. this obviously doesn't make sense, so I assume they kept this data elsewhere (I checked the other two .mdb with mdb-json and it isn't there). easy hack: break these up on " " and organize all the questions into groups according to the first string. will make different decks based on these groups.
                "type":"TEXT",
                "size":44
            }
        ],
        "data":[ ... ]
    }

]

So...
I converted it into the following, saner format:

{
    { // category object
        "name": "coming from Qbook",
        [ // array of questions
            { // question object
                "QuestionCode": int,
                "QuestionText": string,
                "QuestionPhoto": string,
                "CorrectAnswer": int, // index of the correct answer as ordered in the array below.
                [ // array of answers to this question
                    "AnswerText"
                ]
            }
        ]
    }
}