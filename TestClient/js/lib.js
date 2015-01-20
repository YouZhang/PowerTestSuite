function cmdRun(targetFileName){
    var wsh = new ActiveXObject("WScript.Shell");
    var pathName = window.location;
    var fileName = pathName.toString().split("/")[pathName.toString().split("/").length-1];    
    pathName = pathName.toString().replace(fileName,targetFileName);
    if( fileExist(targetFileName) ){
        var result = wsh.run(pathName);
    }
}

function fileExist(fileName){
    var activeObj = new ActiveXObject("Scripting.FileSystemObject");
    if(activeObj.FileExists(abPath() + fileName)){
        return true;       
    }else{
        return false;        
    }        
}
//--
function abPath(){
     var absolutePath = '';
     var pathArray = new Array(); 
     var currentFileLocation = document.location.pathname;      
     pathArray = currentFileLocation.split("/");         
     for(var i = 1; i<pathArray.length-1; i++){                
            absolutePath = absolutePath + pathArray[i] + "\\";
     }
     return absolutePath;
}


function getSelectedVal(i){
    var pullSelect = document.getElementById("TestMode"+i);
    var appendOpt = '1\t{0}\t'.format(pullSelect.value); 
    var restartService = document.getElementById("restartService");
    var regOpt = document.getElementById("regOpt"+i).value;
    if( restartService.checked ){
        appendOpt += "restartService: 1 ";
    }
    var emailCheckBox = document.getElementById('emailCheckBox');
    var emailListObj = document.getElementById('emailList');
    if( emailCheckBox.checked ){
        appendOpt += "emailList: {0} ".format(emailListObj.value);
    }
    // driver = document.getElementById(pullSelect.value+"Driver").value; 
    driverLabel = document.getElementById(i+"Driver").value;
    var runListFileName = generateRunList(pullSelect.value)
    pullSelect = document.getElementById("Codec"+i);
    appendOpt += "{0}: {1}\t".format("Codec",pullSelect.value);
    pullSelect = document.getElementById("App"+i);
    appendOpt += "{0}: {1}\t".format("Application",appArray[pullSelect.value]);
    appendOpt += "{0}: {1}\t".format("RunList",runListFileName);
    if( regOpt != ''){
        appendOpt += "{0}: {1}\t".format("RegFile",regOpt)
    }    
    if( driverLabel != ''){
        appendOpt += "{0}:*{1}".format("Driver",driverLabel)
    }
    appendOpt += '\n';
    return appendOpt;
}


function generateRunList(testMode){

    if( fileExist("RunList\\" + testMode + runListIndex)){
        runListIndex += 1;
    }
    var runListFileName = testMode + runListIndex;
    testModeVal = testModeVal + "1\t" + testMode;
    testModeVal += " RunList: {0}".format(runListFileName)+'\n';
    var currentMode = testMode;
    var runList = document.getElementsByName(currentMode+"Cases");
    var emonList = document.getElementsByName(currentMode + "Emon");
    var powerList = document.getElementsByName(currentMode + "Power");
    var socWatchList = document.getElementsByName(currentMode + "SocWatch");
    var mvpList = document.getElementsByName(currentMode + "MVP");
    var sleepTime = document.getElementById("SleepTime").value;
    if( sleepTime == ''){
        sleepTime = 20;
    }
    var sleepTimeOpt = "sleepTime: " + sleepTime
    for(var j = 0;j < runList.length;j++){
        var optIndex = j;
        if(runList[j].checked){
            caseListVal = caseListVal + "1\t" + runList[j].value + "\t";
            if( emonList[optIndex].checked && j > 0){
                caseListVal = caseListVal + emonList[optIndex].value +':1\t';
            }
            if( powerList[optIndex].checked && j > 0 ){
                caseListVal = caseListVal + powerList[optIndex].value +':1\t';
            }
            if( socWatchList[optIndex].checked && j > 0 ){
                caseListVal = caseListVal + socWatchList[optIndex].value +':1\t';
            }
            if( mvpList[optIndex].checked && j > 0 ){
                caseListVal = caseListVal + mvpList[optIndex].value +':1\t';
            }                        
            caseListVal += sleepTimeOpt + '\n';
        }
        else{
            caseListVal = caseListVal + "0\t" + runList[j].value+"\n";
        }
    }
    writeFile("RunList\\"+runListFileName,caseListVal);
    caseListVal = "";
    return runListFileName;
}

function launch(){    
    var options = new Array("Codec","App","TestMode");
    testModeVal="";
    caseListVal="";
    var testModeList = document.getElementsByName("testMode[]");
    var advConfig = document.getElementById("AdvConfig");
    var codecArray = new Array();
    var testAppArray = new Array();
    var testModeArrat = new Array();
    var appendOpt = '';
    if( advConfig.checked ){        
        for( var i = 1; i <= index; i++ ){
            testModeVal += getSelectedVal(i);
        }
    }
    var indexTimes = 0;
    for (var i = 0; i < testModeList.length;i++ ){
        var pathArray = new Array();
        // driver = document.getElementById(testModeList[i].defaultValue+"Driver").value;        
        if( testModeList[i].checked ){            
            runListFileName = generateRunList(testModeList[i].defaultValue);
            
        }
        else{            
            testModeVal = testModeVal + "0\t" + testModeList[i].value + '\n';
        }
        writeFile("testModeList",testModeVal);        
    }    
    cmdRun("run.bat");
}

function getOptVal(OptName){
    var ret = "";
    var runList = document.getElementsByName(OptName);
    for(var j = 0;j < runList.length;j++){
        if( runList[i].checked ){
            ret = ret + runList[j].value + ":1 ";
        }
    }
    return ret;
}

function writeFile(fileName,content){
    var absolutePath = abPath();
    var targetFile = absolutePath + fileName;
    var activeObj = new ActiveXObject("Scripting.FileSystemObject");
    var file = activeObj.CreateTextFile(targetFile, true);
    file.write(content);
    file.Close();
}

function CheckAll(elementType,ele) {
    var testMode = document.getElementsByName(elementType);
    var i;
    var checkedNum = 0;
    if( ele.checked == true){
        for (i = 0; i < testMode.length; i++) {           
            if(testMode[i].checked == false ){
                testMode[i].checked = true;           
            }
        }       
    }else{
        for (i = 0; i < testMode.length; i++) {
            if( testMode[i].checked == true){
                checkedNum += 1;
            }            
        }
        if( checkedNum == testMode.length){
            for (i = 0; i < testMode.length; i++) {
                testMode[i].checked = false;
            }
        }else{
            for (i = 0; i < testMode.length; i++) {           
                testModeList[i].checked = true;
            }   
        }
    }
}

function Reverse(elementType) {
    var testMode = document.getElementsByName(elementType);
    var i;
    for (i=0; i<testMode.length; i++) {
        testMode[i].click();
    }
}

function setLinkSrc( sStyle ) {	
	document.getElementById( "webfx-tab-style-sheet" ).disabled = sStyle != "webfx"		
	document.body.style.background = sStyle == "webfx" ? "white" : "ThreeDFace";
}

function getFilesFromPath(path){
    var fullPath = abPath() + path;
    var activeObj = new ActiveXObject("Scripting.FileSystemObject");     
    var folderPath = activeObj.GetFolder(fullPath);  
    var fileList = new Enumerator(folderPath.files);
    var folderList = new Enumerator(folderPath.SubFolders);
    var files = new Array();
    for (; !fileList.atEnd(); fileList.moveNext()) {         
        files.push(fileList.item())        
    }        
    for (; !folderList.atEnd(); folderList.moveNext()) {              
        var tempFileList = getFilesFromPath(path + "\\" + folderList.item().Name);
        files = files.concat(tempFileList);
    }    
    return files;
}

function clipFilter(clipList){

    clipTypeSet = new Set();
    vp9ClipList = new Array();
    hevcClipList = new Array();
    otherClipList = new Array();
    for(var i = 0; i < clipList.length;i++){  
        var fileObj = clipList[i];
        var clipName = fileObj.name.split(".")[0];
        var caseContent = '<link rel="stylesheet" type="text/css" href="../css/fullscreen.css" /><video id="video" src="{0}.webm" autoplay></video><script src="../js/localStorge.js"></script>'.format(clipName);
        writeFile("Clips\\"+clipName+'.html',caseContent);
        if( fileObj.type == "WEBM File"){
            vp9ClipList.push(clipName);
            clipTypeSet.add("VP9_Clips");               
        }else if( fileObj.type == "265 File"){
            hevcClipList.push(clipName);
            clipTypeSet.add("HEVC_Clips");                
        }else if( fileObj.type != "HTML Document"){
            otherClipList.push(clipName);
            clipTypeSet.add("Other_Clips");
        }
    }
    res = {"clipTypeSet":clipTypeSet,"vp9ClipList":vp9ClipList,"hevcClipList":hevcClipList,"otherClipList": otherClipList};
    return res;
}

String.prototype.format= function(){
    var args = arguments;
    return this.replace(/\{(\d+)\}/g,function(s,i){
     return args[i];
    });
}

function plotUI(clipInfo){
    
    options = new Array("Codec","App","TestMode");
    optXMLFiles = new Array("codecOpt.xml","testAppOpt.xml","testModeConfig.xml");
    testModeList = addSelectOpt("testMode","testModeConfig.xml");
    // testModeList = new Array("VP9FixedPlayback","VP9FixedChrome","VP9FreePlayback","HEVCFixedPlayback","FFPlay","FFMpeg","PotPlayer32","PotPlayer64","VP9FreeDecode");
    //load header
    document.write('<html><head><title>Codec PnP Test Suite Author : You Zhang</title><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />');
    //load css;
    document.write('<link id="webfx-tab-style-sheet" type="text/css" rel="stylesheet" href="css/tab.webfx.css" disabled="disabled" /><link rel="stylesheet" type="text/css" href="css/local.css" /><link rel="stylesheet" type="text/css" href="css/downPull.css" />');
    //load js
    document.write('<script type="text/javascript" src="local/webfxlayout.js"></script><script type="text/javascript" src="js/tabpane.js"></script><script type="text/javascript" src="js/lib.js"></script><script type="text/javascript" src="local/webfxlayout.js"></script><script type="text/javascript" src="js/downPull.js"></script></head><body>');
    //select css
    document.write('<script type="text/javascript">setLinkSrc( "webfx" );</script>');
    document.write('<style>p{text-align:center}</style>');
    //header 1
    document.write('<br><li><b>STEP 1: Select Your Test Mode</b></li><br><br>');
    //load tab1    
    
    //load tab1 option
    addTab1( testModeList,options);
    // document.write('<input type="checkBox" name="selectAll" onclick=\'CheckAll("testMode[]");\' id="select_all">SelectAll<br><input type="checkBox" name="selectedInverse" onClick=\'Reverse("testMode[]");\' id="inv_select_all">InverseSelect<br><hr style="border:4px double #e8e8e"/><input type="checkBox" name="testMode[]" value="VP9FixedPlayback"/>VP9FixedPlayback<br><input type="checkBox" name="testMode[]" value="VP9FixedChrome" />VP9FixedChrome<br><input type="checkBox" name="testMode[]" value="VP9FreePlayback"/>VP9FreePlayback<br><input type="checkBox" name="testMode[]" value="HEVCFixedPlayback"/>HEVCFixedPlayback<br></div></div>');    
    //load title for tab2
    document.write('<br><li><b>STEP 2: Select Your Case </b></li><br><br>');
    //
    addTab2(clipInfo,testModeList);    
    //addButton
    
    document.write('<p><input type="button" class="button" value="R u n" onclick="launch()"/><br></p>');
    //init 
    document.write('<script type="text/javascript">setupAllTabs();</script></body>')

    
}

function addSelectOpt(selectId,xmlFile){  
    var select = document.getElementById(selectId);
    var xmlDoc = new ActiveXObject("Microsoft.XMLDOM");
    var ret = new Array();
    var xmlFilePath = "configXML\\" + xmlFile;
    xmlDoc.async="false";
    xmlDoc.load(xmlFilePath);
    root = xmlDoc.documentElement;
    var nodes = root.childNodes;
    for(var i = 0; i < nodes.length;i++){
        var opt = document.createElement("option");
        opt.value = nodes.item(i).nodeName;
        opt.innerHTML = opt.value;
        ret.push(opt.value);
        try{
            select.appendChild(opt);
        }catch(e){}
    }
    return ret;
}

function addSelection(options){    
    var content = '';
    for ( var i = 0; i < options.length;i++){
        content += '<b>{0}:</b> <SELECT id=\'{1}\'></SELECT>&nbsp;&nbsp;&nbsp;&nbsp'.format(options[i],options[i]+index);
    }
    content += '<br>'
    content += addDriverChangeCase(index,0)
    content += addRegOpt(index)
    return content;
}

function highlightTab(pullSelect){
    var pageArray = tp2.pages;
    for(var i = 0; i < pageArray.length;i++){
        className = pageArray[i].tab.className;
        if( pullSelect.value == pageArray[i].aElement.innerText ){
            pageArray[i].tab.className = 'tab highlight';
        }
    }
}
function cancelHighlight(testmode){
    var pageArray = tp2.pages;
    for(var i = 0; i < pageArray.length;i++){
        className = pageArray[i].tab.className;
        if( testmode == pageArray[i].aElement.innerText ){
            pageArray[i].tab.className = 'tab';
        }
    }
}


function addSelectContent(){
    appArray = new Array();
    for ( var i = 0; i < options.length;i++){
        if( options[i] == "App"){
            var fileArray = getFilesFromPath("app");
            for( var j = 0;j < fileArray.length;j++){
                if( fileArray[j].type == "Application" || fileArray[j].type == "Shortcut"){
                    appArray[fileArray[j].Name] = fileArray[j].Path;
                    var select = document.getElementById(options[i]+index);
                    var opt = document.createElement("option");
                    opt.value = fileArray[j].Name;
                    opt.innerHTML = opt.value;
                    select.appendChild(opt); 
                }
            }
        }else if(options[i] == "TestMode"){
            testModeList = addSelectOpt(options[i]+index,optXMLFiles[i]);
        }else{
            addSelectOpt(options[i]+index,optXMLFiles[i]);
        }
    }    
}

function addTab1(testModeList,options){
    
    content = '<div class="tab-pane" id="tabPane1"><script type="text/javascript">tp1 = new WebFXTabPane( document.getElementById( "tabPane1" ) );</script><div class="tab-page" id="tabPage1"><h2 class="tab">Basic Mode</h2><script type="text/javascript">tp1.addTabPage( document.getElementById( "tabPage1" ) );</script>';

    // content += '<SELECT id="demo_select" NAME=""></SELECT><br>';
       
    content += '<input type="checkBox" name="Tab1selectAll" onclick=\'CheckAll("testMode[]",this);\' id="Tab1selectAll">SelectAll<br>';
    content += '<input type="checkBox" name="Tab1selectedInverse" onClick=\'Reverse("testMode[]");\' id="Tab1inv_select_all">InverseSelect<br>';    
    content += '<hr style="border:4px double #e8e8e"/>';   
    for( var i = 0; i < testModeList.length ; i++){
        content += '<input type="checkBox" onchange=\'checkBoxStatus(this);\' name="testMode[]" value=\'{0}\'/>{1}<br>'.format(testModeList[i],testModeList[i]);        
    }
    content += '</div>';
    content += '<div class="tab-page">';
    content += '<input type="checkBox" id="AdvConfig" onchange=\'checkBoxStatus(this);\' value=\'{0}\'/><b>Enable Advanced Mode</b> -> use the specific app to run case<br>';
    content += '<input type="checkBox" id="restartService" value=\'{0}\'/><b>Enable Restart Service</b> -> Restart after finshing every single case<br>';
    content += addEmailList();
    content += addSleepTimeOpt();
    content += '<h2 class="tab">Advanced Mode</h2>';
    content += '<div id="pullSelect">';    
    content += '<hr style="border:4px double #abcdef"/><br>';
    content += addSelection(options);      
    content += '</div><br>';        
    content += '<input type="button" class="button" id="addSelectionButton" value="AddTestMode"/>';
    content += '<input type="button" align="right" value="confirmTestMode" class="button" onclick="confirmTestMode()"/><br><br>'
    content += '<hr style="border:4px double #abcdef"/>';
    content += '</div></div>';
    document.write(content);    
}

function addEmailList(){
    var content = "";
    content += '<input type="checkBox" id="emailCheckBox" value="emailCheckBox"/><b>Enable Email Config : &nbsp;&nbsp;&nbsp;&nbsp;</b>'
    content += '<input size=50 name="Email" type="text" id="emailList" placeholder="xxx@intel.com,yyy@intel.com"><br>'
    return content;    
}

function confirmTestMode(){
    for (var i = 0; i < testModeList.length;i++){
        cancelHighlight(testModeList[i]);
    }
    for (var i = 1; i <= index;i++){
        var pullSelect = document.getElementById("TestMode"+i);
        highlightTab(pullSelect);
    } 
    var advConfig = document.getElementById("AdvConfig");
    advConfig.checked = true;
    checkBoxStatus(advConfig);
}

function addTab2(clipInfo,testModeList){
    var clipTypeSet = clipInfo.clipTypeSet;
    var vp9ClipList = clipInfo.vp9ClipList;
    var hevcClipList = clipInfo.hevcClipList;
    var otherClipList = clipInfo.otherClipList;    
    testOptList = new Array("Cases","Emon","Power","SocWatch","MVP");
    content = '<div class="tab-pane" id="tabPane2"><script type="text/javascript">tp2 = new WebFXTabPane( document.getElementById( "tabPane2" ) );</script>';
        
    for( var i = 0;i < testModeList.length;i++){
        content += '<div class="tab-page" id="{0}">'.format(testMode);        
        var testMode = testModeList[i];
        content += '<h2 class="tab">{0}</h2>'.format(testMode);
        content += '<script type="text/javascript">tp2.addTabPage( document.getElementById( "{0}" ) );</script>'.format(testMode);
        for( j = 0;j < testOptList.length;j++){
            var testOpt = testOptList[j];
            // add select all;
            content += '<input type="checkBox" name="selectAll" onclick=\'CheckAll("{0}",this);\' id="select_all">SelectAll{1}'.format(testMode+testOpt,testOpt);        
            //add inv select all;
            content += '<input type="checkBox" name="selectedInverse" onClick=\'Reverse("{0}");\' id="inv_select_all">InvSelect{1}'.format(testMode+testOpt,testOpt);                      
            //add br
            content += '<br>';
        }
        //add line
        content += '<hr style="border:4px double #abcdef"/>';
        //add driver change case;
        // content += addDriverChangeCase(testMode,"Cases");
        //add cases;
        //add new sub tab
        content += '<div class="tab-pane" id="tabPane4">';        
        clipTypeSet.forEach(function(clipType){
			content += '<div class="tab-page"><h2 class="tab">{0}</h2>'.format(clipType);
            if( clipType == "VP9_Clips"){
                clipList = vp9ClipList;
            }else if(clipType == "HEVC_Clips"){
                clipList = hevcClipList;
            }else{
                clipList = otherClipList;
            }

            clipListDict = getDiffResClips(clipList);
            for ( var clipListName in clipListDict ){
                
                var len = clipListDict[clipListName].length;
                if( len > 0){             
                    //add header
                    var height = len * 60;
                    var id = clipListName + clipType + testMode
                    
                    content += '<div id="control"><table width="100%"  border="0" cellpadding="0" cellspacing="0"><tr>';
                    
                    content += '<td width="100%" align="center" class="tabTit" onClick="Effect(\'{0}\',{1});" ><li id="{2}tab" style="float:right"><a href="#" >+</a> </li><li style="float:left"><a href="#" class="testLink">{3}</a> </li></td></tr></table>'.format(id,height,id,clipListName);
                    
                    content += '</div>';
                    
                    content += '<div id="{0}" class="test" style="display:none;"><table width="100%"  border="0" cellpadding="4" cellspacing="0" bgcolor="#EEEEEE"><tr>'.format(id);                   
                    
                    // content += '<hr style="border:3px dotted #000 "/><p align="center"><b><font style="color:red;font-size:16px;">{0}</font></b></p><hr style="border:3px dotted #000 "/>'.format(clipListName);
                    addCaseOpt(clipListDict[clipListName],testMode,testOptList);
                    content += '</tr></table></div>';
                }
            }         
            content += '</div>';
        })
        content += '</div></div>';        
    }
    content += '</div>';
    document.write(content);
}


function getDiffResClips(clipList){
    fourKClipList = new Array();
    fullHDClipList = new Array();
    otherClipList = new Array();
    for( var index in clipList) {
        var clip = clipList[index];
        if( clip.indexOf("2160p") > 0){
            fourKClipList.push(clip);
        }else if( clip.indexOf("1080p") > 0){
            fullHDClipList.push(clip);
        }else{
            otherClipList.push(clip);
        }
    }
    return {"fourKClipList":fourKClipList,"fullHDClipList":fullHDClipList,"otherClipList":otherClipList};    
}
function addCaseOpt(clipList,testMode,testOptList){
    for( k = 0; k < clipList.length;k++){
        var clip = clipList[k];
        for( j = 0;j < testOptList.length;j++){
            var testOpt = testOptList[j];
            if(testOpt == "Cases"){
                content += '<input type="checkBox" name="{0}" value="{1}"/><b>{2}</b><br>'.format(testMode+testOpt,clip,clip);
            }else{
                content += '<input type="checkBox" name="{0}" value="{1}"/>{2}'.format(testMode+testOpt,testOpt,testOpt);
            }                
        }
        content += '<hr style="border:4px double #e8e8e8"/>';
    }
}
function addDriverChangeCase(flag,testOpt){
    content = "";
    // content += '<input type="checkBox" name="{0}" value="Change_Driver"/><b>Change_Driver</b>'.format(testMode+testOpt);
    content += '<b>Driver: </b><input size=42 name="Driver" type="text" id="{0}Driver" placeholder="Example:ci-gen8_2014-29500 Release 64-bit">&nbsp'.format(flag);
    // content += '<hr style="border:4px double #abcdef"/>';
    return content;
}

function addSleepTimeOpt(){
    content = "";
    content += '<input type="checkBox" name="Sleep_Time_Setting" value="Sleep_Time_Setting"/><b>Enable Interval Config : </b>';
    content += '<input size=50 name="SleepTime" type="text" id="SleepTime" placeholder="please input interval time between cases, eg. 20"><br>';
    return content;
}

function addRegOpt(flag){
    content = "";
    content += '<b>RegKey Config : </b>';
    content += '<input size=42 name="reg" type="text" id="regOpt{0}" placeholder="input your reg file,eg. vp9h.reg;hevch.reg">'.format(flag);
    return content;
}

function setLinkSrc( sStyle ) {	
    document.getElementById( "webfx-tab-style-sheet" ).disabled = sStyle != "webfx"		
    document.body.style.background = sStyle == "webfx" ? "white" : "ThreeDFace";
}

function checkBoxStatus(element){
    var finishStepOne = false;
    testOptList = new Array("Cases","Emon","Power","SocWatch","MVP");
    if( element.checked == true ){
        finishStepOne = true;
    }
    if( !finishStepOne ){
        for( var i = 0;i < testOptList.length; i++){
            var inputObjList = document.getElementsByName(element.defaultValue+testOptList[i]);
            for( var j = 0; j < inputObjList.length; j++){                        
                inputObjList[j].disabled = true;
            }
        }     
    }else{
        if( element.id == "AdvConfig"){
            var inputObjList = document.getElementsByTagName("input");
            for( var j = 0; j < inputObjList.length; j++){                        
                inputObjList[j].disabled = false;
            }        
        }else{
            for( var i = 0;i < testOptList.length; i++){        
                var inputObjList = document.getElementsByName(element.defaultValue+testOptList[i]);
                for( var j = 0; j < inputObjList.length; j++){                        
                    inputObjList[j].disabled = false;
                }
            }        
        }
                
    }      
}


function del(o){
    for(var i = 1; i <= testModeList.length;i ++){
        var pullSelect = document.getElementById("TestMode"+i);
        if( pullSelect == null) break;
        cancelHighlight(pullSelect.value);
    }    
    document.getElementById("pullSelect").removeChild(document.getElementById("testConfig"+o));
    index -= 1;
    confirmTestMode()
}

index = 1;
runListIndex = 0;
// function addContent(){
    // i = 1;
    // document.getElementById("addSelectionButton").onclick=function(){
    // document.getElementById("pullSelect").innerHTML+='<div id="div_'+i+'"><input name="text" name="text_'+i+'" type="text" value="test"  /><input type="button" value="delete"  onclick="del('+i+')"/></div>';
    // i = i + 1;
    // }
// }