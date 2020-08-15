function takePicture() {
    document.getElementById('videofeed.container').innerHTML = '';
    setTimeout(function() {
        postRequest("/control/camera/", "MODE=picture")
        setTimeout(function() {document.getElementById('videofeed.container').innerHTML = "<img src='/video_feed' width='360' height='480'>";}, 3000)
    }, 3000);

}
