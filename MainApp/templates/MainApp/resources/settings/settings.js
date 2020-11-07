function isIE() {
    //ZJ3: The below code is referred from http://stackoverflow.com/questions/9847580/how-to-detect-safari-chrome-ie-firefox-and-opera-browser
    //Do not know exactly how it works but test results are good
    return (false || !!document.documentMode);
}

function getObject() {
    var myObject;
    if (isIE())
        myObject = document.getElementById('_ComposerPlayerActiveX');
    else
        myObject = document.getElementById('_ComposerPlayerPlugin');

    return myObject;
}

function getObject2() {
    var myObject2;
    if (isIE())
        myObject2 = document.getElementById('_ComposerPlayerActiveX2');
    else
        myObject2 = document.getElementById('_ComposerPlayerPlugin2');

    return myObject2;
}

function addEvent(obj, name, func) {
    if (obj.attachEvent)
        obj.attachEvent(name, func);
    else
        obj.addEventListener(name, func, false);
}

function setBackgroundImage(object, div) {
    var imagePath = myObject.GetTempFolder() + new Date().getTime() + ".jpg";
    object.SaveImageFullViewport(imagePath);
    imagePath = "file:///" + imagePath;
    imagePath = imagePath.replace(/[\\]/g, "\/");
    el = document.getElementById(div);
    el.style.backgroundImage = "url(" + imagePath + ")";
    object.style.visibility = "hidden";
}
