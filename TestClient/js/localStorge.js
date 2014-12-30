video = document.getElementById("video");
var vLength;
storage = window.localStorage;
if (!storage.getItem(video.src)){
    storage.setItem(video.src,0);
}

video.onloadedmetadata = function () { 
    startDate=new Date();
    vLength = video.duration;     
};

video.ontimeupdate = function () { 
    var vTime = video.currentTime 
    if( vLength == vTime){
        var endDate=new Date();
        var deltaTime = endDate.getTime() - startDate.getTime();
        var displayFrame = video.webkitDecodedFrameCount - video.webkitDroppedFrameCount;
        var decodeFPS = video.webkitDecodedFrameCount / deltaTime * 1000;
        var droppedFrameRate = video.webkitDroppedFrameCount/ video.webkitDecodedFrameCount;
        storage.setItem(video.src,"decodeFPS: " + decodeFPS + " droppedFrameRate: " + droppedFrameRate); 
        closeWindow();
    }
};

function sleep(){}

function closeWindow() 
{
  window.opener = null;
  window.open(' ', '_self', ' ');  
  window.close();
}

function showStorage(){
    for(var i=0;i<storage.length;i++){  
        document.write(storage.key(i)+ " : " + storage.getItem(storage.key(i)) + "<br>");
    }
}