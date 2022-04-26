console.log("I am so sleepy");

document.getElementById('originalImageFile').addEventListener('change', function () {
    if (this.files[0]) {
        var picture = new FileReader();
        picture.readAsDataURL(this.files[0]);
        picture.addEventListener('load', function (event) {
            document.getElementById('badnamingconventions').setAttribute('src', event.target.result);
            document.getElementById('sleepy').style.display = 'block';
            // document.getElementById('ireallyamsosleepythough').setAttribute('src', event.target.result);
            console.log("ok this works")
        });
    }
});

async function postData(url = 'localhost:5000/api/process', data = {}) {
    // Default options are marked with *
    const file = data.image
    const formData = new FormData();
    formData.append('image', file)
    formData.append('type', data.type)
    const response = await fetch(url, {
        method: 'POST',
        body: formData // body data type must match "Content-Type" header
    });
    console.log(response)
    return response; // parses JSON response into native JavaScript objects
}


function ihopethisworks(ev) {
    ev.preventDefault();
    let form = new FormData(ev.target);
    let visiontype = (form.get("colorBlindDropDown"));
    let image = (form.get("originalImageFile"));
    let jsonsrkinddumb = {
        type: visiontype,
        image: image
    }
    console.log(jsonsrkinddumb)
    console.log("see, it works, u chose option ", jsonsrkinddumb["type"]);

    postData('http://localhost:5000/api/process', jsonsrkinddumb)
    .then(response => response.blob())
    .then(blob => {
        objUrl = URL.createObjectURL(blob);
        document.getElementById('ireallyamsosleepythough').setAttribute('src', objUrl)
    })
        // .then(data => {
        //     console.log(data); // JSON data parsed by `data.json()` call
        // });
}