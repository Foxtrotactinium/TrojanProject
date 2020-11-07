////display meta properties////
var pp
function Displayallmetas(actor)
{

document.getElementById('Meta_container').innerHTML='<table id="meta_list" border="0" cellspacing="3"></table>'   //clear the table

var allprop=myObject.GetProperties(actor,0,0)

test_has_meta=allprop.indexOf("Meta.")

if(test_has_meta!=-1)
{
  tableformeta = allprop.split("Meta.") //displays all properites containing "meta"//
  
  
  var size=tableformeta.length
  for (pp = 1;pp<=(size-1);pp++)
  {
    var metadef=tableformeta[pp].indexOf(" ")
    var metadef1=tableformeta[pp].substring(0,metadef)
  
  do
  {
    metadef1=metadef1.replace("_"," ")
    var is_there_underscore=metadef1.indexOf('_')
  }
  while(is_there_underscore!=(-1))
  
  
  var metavaluepos1=tableformeta[pp].indexOf("=")
  var metavaluepos2=tableformeta[pp].indexOf("/>")
  var metavalue=tableformeta[pp].substring(metavaluepos1+2,metavaluepos2-1)
  
  myNewRowmeta1 = document.getElementById("meta_list").insertRow(pp-1); //add a new line to the table each time
  
  //name of meta//
  myNewCellmeta1=myNewRowmeta1.insertCell(0)
  myNewCellmeta1.id="def"+metadef1
  document.getElementById(myNewCellmeta1.id).width="150px"
  document.getElementById(myNewCellmeta1.id).innerHTML="<b>"+metadef1+"<b>"
  
  //value of meta//
  myNewCellmeta2=myNewRowmeta1.insertCell(1)
  myNewCellmeta2.id="value"+metadef1
  document.getElementById(myNewCellmeta2.id).width="100%"
  document.getElementById(myNewCellmeta2.id).innerHTML=metavalue
  }
//$('#Meta_zone').jScrollPane({showArrows:true,horizontalGutter:10});
}
//////////////////////////////////

}
