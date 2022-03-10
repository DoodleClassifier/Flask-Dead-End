fetch('/test')
    .then(function (response) {
        return response.json();
    }).then(function (text) {
        console.log('GET response:');
        console.log(text.greeting); 
    });

fetch('/test-model')
    .then(function (response) {
        return response.json();
    }).then(function (predictions) {
        console.log("Done testing!");
        console.log(predictions)
    })

