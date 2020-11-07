// JavaScript Document


var all_CAD_Captures_Id
var CAD_Capture_Id
var all_CAD_Captures
var CAD_Capture_array
var CAD_Capture= new Array()
var CAD_View_children_Name = new Array()
var PMI_Element=new Array()
var CAD_Capture_Element=new Array()
var PMI_List_for_Color_change=""

function Build_PMI_table()
{
document.getElementById("PMI_Table_div").innerHTML='<div id="capture"><img src="resources/modules/m_tree/img/root.png" title="root" height="15" width="15"> <span id="p-capture"></span>  </div><table id="PMI_Table" border="0" cellspacing="0" cellpadding="0"></table>'

//////CAD Capture ID////////
myObject.UseGUID = 1;
all_CAD_Captures_Id=myObject.GetCADCaptures()
var sup_pos=all_CAD_Captures_Id.indexOf('>')
var pound_pos=all_CAD_Captures_Id.lastIndexOf('#')
all_CAD_Captures_Id=all_CAD_Captures_Id.substring(sup_pos+1,pound_pos)
CAD_Capture_Id=all_CAD_Captures_Id.split('#')
/////////////////////////////


//////CAD Capture Name////////
myObject.UseGUID = 0;
all_CAD_Captures=myObject.GetCADCaptures()
CAD_Capture_array=all_CAD_Captures.split('CLitModifiable Name=')

for (i = 1;i<=CAD_Capture_array.length-1;i++) 
{
var sign_pos=CAD_Capture_array[i].indexOf('/>')
CAD_Capture[i-1]=CAD_Capture_array[i].substring(1,sign_pos-1)
}
/////////////////////////////

CAD_Capture_Element=multisort(new Array(CAD_Capture,CAD_Capture_Id),1)


for (j=0;j<=CAD_Capture.length-1;j++)
//for (j=0;j<=2;j++)
{

var New_CAD_Capture_Row = document.getElementById("PMI_Table").insertRow(2*j);

var Eye_Cell=New_CAD_Capture_Row.insertCell(0);
Eye_Cell.id='CADEye_'+CAD_Capture_Element[1][j];
//alert('<img id="Img_'+CAD_Capture_Id[j]+'" onclick="javascript:Hide_PMI_List(\"'+CAD_Capture_Id[j]+'\");" src="images/closed.gif"/>')
document.getElementById('CADEye_'+CAD_Capture_Element[1][j]).innerHTML="<img id='Img_Closed_"+CAD_Capture_Element[1][j]+"\' onclick='javascript:Show_PMI_List(\""+CAD_Capture_Element[1][j]+"\");' src='resources/img/closed.gif'/><img style='display:none;' id='Img_Open_"+CAD_Capture_Element[1][j]+"\' onclick='javascript:Hide_PMI_List(\""+CAD_Capture_Element[1][j]+"\");' src='resources/img/open.gif'/>";




var New_CAD_Capture_Cell=New_CAD_Capture_Row.insertCell(1);
New_CAD_Capture_Cell.id='CADId_'+CAD_Capture_Element[1][j];
New_CAD_Capture_Cell.name='CADName_'+CAD_Capture_Element[1][j];
document.getElementById('CADId_'+CAD_Capture_Element[1][j]).style.fontSize = "11px";
document.getElementById('CADId_'+CAD_Capture_Element[1][j]).style.fontWeight="bold"  
document.getElementById('CADId_'+CAD_Capture_Element[1][j]).innerHTML="<a onclick=\"javascript:Launch_CAD_View('ref:netguid:"+CAD_Capture_Element[1][j]+"');\">"+CAD_Capture_Element[0][j]+"</a>"


var New_PMI_List_Row = document.getElementById("PMI_Table").insertRow(2*j+1);

var Line_Cell=New_PMI_List_Row.insertCell(0);
Line_Cell.id='Line_'+CAD_Capture_Element[1][j];
document.getElementById('Line_'+CAD_Capture_Element[1][j]).style.verticalAlign='top'
document.getElementById('Line_'+CAD_Capture_Element[1][j]).innerHTML='<img class="test" style="display:none;" id="Img_doc2'+CAD_Capture_Element[1][j]+'" src="resources/img/doc2.gif"/>';


var New_PMI_Cell=New_PMI_List_Row.insertCell(1);
New_PMI_Cell.id='PMI_Id_'+CAD_Capture_Element[1][j];
document.getElementById('PMI_Id_'+CAD_Capture_Element[1][j]).innerHTML='<div style="display:none;" id="PMI_List_div'+CAD_Capture_Element[1][j]+'"><table class="PMI_lines" id="PMI_List_'+CAD_Capture_Element[1][j]+'" border="0" cellspacing="0" cellpadding="0"></table></div>'


/////CAD Capture Children ID///////
myObject.UseGUID = 1;
var Current_CAD_View_children_List=myObject.GetChildren('<CLitSelection>'+CAD_Capture_Element[1][j]+'</CLitSelection>',-1)


if(Current_CAD_View_children_List.indexOf('&')!=(-1))
{
Current_CAD_View_children_List=Current_CAD_View_children_List.replace('&','and')
}


var sup_pos1=Current_CAD_View_children_List.indexOf('>')
var pound_pos1=Current_CAD_View_children_List.lastIndexOf('#')
Current_CAD_View_children_List=Current_CAD_View_children_List.substring(sup_pos1+1,pound_pos1)
CAD_View_children_Id=Current_CAD_View_children_List.split('#')
////////////////////////////////////


/////CAD Capture Children Name///////
myObject.UseGUID = 0;
var Current_CAD_View_children_List_Name=myObject.GetChildren('<CLitSelection>'+CAD_Capture_Element[1][j]+'</CLitSelection>',-1)
var sup_pos2=Current_CAD_View_children_List_Name.indexOf('>')
var sign_pos2=Current_CAD_View_children_List_Name.lastIndexOf('/>')
Current_CAD_View_children_List_Name=Current_CAD_View_children_List_Name.substring(sup_pos2+1,sign_pos2+2)
var CAD_View_children_Name_bis=Current_CAD_View_children_List_Name.split('CLitModifiable Name')


for (z = 1;z<=CAD_View_children_Name_bis.length-1;z++) 
{
var equal_pos=CAD_View_children_Name_bis[z].indexOf('=')
var sign_pos3=CAD_View_children_Name_bis[z].indexOf('/>')
CAD_View_children_Name[z-1]=CAD_View_children_Name_bis[z].substring(equal_pos+2,sign_pos3-1)
}

PMI_Element=multisort(new Array(CAD_View_children_Name,CAD_View_children_Id),1)

for (g = 1;g<=CAD_View_children_Name_bis.length-1;g++) 
{

  var PMI_or_not=myObject.IsCollaboration('<CLitSelection>'+PMI_Element[1][g-1]+'</CLitSelection>')
  if(PMI_or_not==true)
  {
  var New_PMI_Line = document.getElementById('PMI_List_'+CAD_Capture_Element[1][j]).insertRow(0);
  
  var PMI_Decription_Cell=New_PMI_Line.insertCell(0);
  PMI_Decription_Cell.id='PMI_Decription_'+j+PMI_Element[1][g-1];
  document.getElementById('PMI_Decription_'+j+PMI_Element[1][g-1]).innerHTML="<a onclick=\"javascript:Zoom_Annotation('"+PMI_Element[1][g-1]+"');\" onmouseover=\"javascript:Highlight_PMI('"+PMI_Element[1][g-1]+"')\">"+PMI_Element[0][g-1]+"</a>"
  
  PMI_List_for_Color_change=PMI_List_for_Color_change+PMI_Element[1][g-1]+'#'
  
  }
}


///////////////////////////////////
myObject.UseGUID = 1;

}

//$('#PMI_Table_div').jScrollPane({showArrows:true,horizontalGutter:10});

}


function Zoom_Annotation(Annot_Id)
{
  if(is_3d_window==1) //if there is a detail view, this shows the detail in it. If not, this shows in the main scene.
  {
  //select_to_highligh_Tree=1;
    myObject2.SetVisibility('<CLitSelection Name="">'+Annot_Id+'</CLitSelection>',1,2);
    myObject2.ZoomFitAll();
  }
  else
  {
    myObject.Selection = '<CLitSelection>'+Annot_Id+'</CLitSelection>';
  }

/*myObject.ZoomSelection();
myObject.RefreshScene(1);*/
}


function Highlight_PMI(Annot_Id)
{
myObject.HighlightedObject = '<CLitSelection>'+Annot_Id+'</CLitSelection>';
}

function Hide_PMI_List(CAD_Id)
{
document.getElementById('PMI_List_div'+CAD_Id).style.display="none";
document.getElementById('Img_Open_'+CAD_Id).style.display="none";
document.getElementById('Img_Closed_'+CAD_Id).style.display="block";
document.getElementById('Img_doc2'+CAD_Id).style.display="none";
//$('#PMI_Table_div').jScrollPane({showArrows:true,horizontalGutter:10});
}


function Show_PMI_List(CAD_Id2)
{
document.getElementById('PMI_List_div'+CAD_Id2).style.display="block";
document.getElementById('Img_Closed_'+CAD_Id2).style.display="none";
document.getElementById('Img_Open_'+CAD_Id2).style.display="block";
document.getElementById('Img_doc2'+CAD_Id2).style.display="block";
//$('#PMI_Table_div').jScrollPane({showArrows:true,horizontalGutter:10});
}

function Launch_CAD_View(CAD_View_Name)
{
myObject.GoToView(CAD_View_Name);
}





