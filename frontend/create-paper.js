function uploadDoc(){

    let subject = document.getElementById("subject").value;
    let fileInput = document.getElementById("fileInput");

    if(subject === "" || fileInput.files.length === 0){
        alert("Enter subject and select file");
        return;
    }

    let formData = new FormData();
    formData.append("subject", subject);
    formData.append("file", fileInput.files[0]);

    fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("uploadMsg").innerText = data.message;
    })
    .catch(err => {
        document.getElementById("uploadMsg").innerText = "Upload Failed";
    });
}
