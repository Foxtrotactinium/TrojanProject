// JavaScript Document

function init_BOM()
{
var root=myObject.GetAssyRoot();

var root_pos1=root.indexOf('>');
root=root.slice(root_pos1+1);
var root_pos2=root.indexOf('#<');
root=root.substring(0,root_pos2);
var root_ids=root.split("#");

number_of_child_in_root=root_ids.length ;

Element_Name=new Array()
Element_Id=new Array()
Element_Bomid=new Array()

get_all_assys_and_parts(root_ids,number_of_child_in_root);
Analyse_quantity();
Build_Bom('no');

}


var Element_Name=new Array()
var Element_Id=new Array()
var Element_Bomid=new Array()
var t=0;
var Number_of_parts=0;
function get_all_assys_and_parts(Actor_Id,NumberOfChild)
{

var i
for (i = 0;i<=(NumberOfChild-1);i++)
{
var iscollab=myObject.IsCollaboration('<CLitSelection Name="">'+Actor_Id[i]+'</CLitSelection>')

  if(iscollab==false)
  {
  
  
    var get_name = new get_property('<CLitSelection Name="">'+Actor_Id[i]+'</CLitSelection>',"Actor.Name");
    var actorname=get_name.get_property_value() 
  
    var bValue = myObject.AllNameOccurences;
    myObject.AllNameOccurences = 0;

    var get_BOMid = new get_property('<CLitSelection Name="">'+Actor_Id[i]+'</CLitSelection>',"Actor.BomId");
    var element_Bomid = get_BOMid.get_property_value()

    myObject.AllNameOccurences = bValue;
    
    
    
    
    if (element_Bomid != "" && myObject.GetVisibility('<CLitSelection Name="">' + Actor_Id[i] + '</CLitSelection>') != 2)
    {
    Element_Name[t]=actorname;
    Element_Id[t]=Actor_Id[i];
    Element_Bomid[t]=element_Bomid;
    t+=1;
    Number_of_parts+=1;
    }
  
    var has_child=myObject.HasChilds('<CLitSelection Name="">'+Actor_Id[i]+'</CLitSelection>')
    if (has_child==false)
    {;}
    else
    {
    var child=myObject.GetAssyChild('<CLitSelection Name="">'+Actor_Id[i]+'</CLitSelection>'); 
    var child_pos1=child.indexOf('>');
    child=child.slice(child_pos1+1);
    var child_pos2=child.indexOf('#<');
    child=child.substring(0,child_pos2);
    var child_ids=child.split("#");
    number_of_child=child_ids.length ;
    
    get_all_assys_and_parts(child_ids,number_of_child);
    }
  
  }
}

}

var Part_name_with_qtity=new Array()
var Part_Bom_with_qtity=new Array()
var Part_qtity=new Array()
var Part_Id_with_qtity=new Array()
var Part_full_information=new Array()
var new_position
function Analyse_quantity()
{

Part_name_with_qtity=new Array()
Part_Bom_with_qtity=new Array()
Part_qtity=new Array()
Part_Id_with_qtity=new Array()
Part_full_information=new Array()

new_position=0

//this sorts the array in order to order the BOM id. This will be helpful to identify the BOM id that are repeated
var sorted_BOM=multisort(new Array(Element_Bomid,Element_Name,Element_Id),2)

var Double_BOM=0
var Id_for_doubled_BOM=""
for (l = 0;l<=Number_of_parts-1;l++)
{

if(sorted_BOM[0][l]==sorted_BOM[0][l+1])
{
Double_BOM=Double_BOM+1
//For the Part that have he same Bom id, a new variable is created. This variable is a concatenation of the ID of the part that have the same BOMId
Id_for_doubled_BOM=sorted_BOM[2][l]+"#"+Id_for_doubled_BOM  
}
else
{
// this create new arrays depending on the pre-existance of the Bom Id
  if(Double_BOM>0)
  {
  Part_name_with_qtity[new_position]=sorted_BOM[1][l]
  Part_Bom_with_qtity[new_position]=sorted_BOM[0][l]
  Part_qtity[new_position]=(Double_BOM+1)
  Part_Id_with_qtity[new_position]=Id_for_doubled_BOM+sorted_BOM[2][l]
  Double_BOM=0
  Id_for_doubled_BOM=""
  }

  else
  {
  Part_name_with_qtity[new_position]=sorted_BOM[1][l]
  Part_Bom_with_qtity[new_position]=sorted_BOM[0][l]
  Part_qtity[new_position]=1
  Part_Id_with_qtity[new_position]=sorted_BOM[2][l]
  }

new_position=new_position+1

}

}
Part_full_information=new Array(Part_name_with_qtity,Part_Bom_with_qtity,Part_qtity,Part_Id_with_qtity)
}


var array_sorted=0
function Build_Bom(add_meta)
{
var BOM_table_width=300;
var table_titles='<th><img onclick="Javascript:Meta_win();" style="float:left;cursor:pointer;" src="resources/img/add.png" height="14px" width="14px" title="Configure Columns" >Name</th><th>Id</th><th>Qty</th>'    
if(add_meta=='yes')
{

for (p = 1;p<=meta_name.length-1;p++)
  {
  if (document.getElementById(meta_name[p]).checked==true)
    { 
      var get_meta = new get_property('<CLitSelection Name="">'+test_id+'</CLitSelection>','Meta.'+meta_name[p]);
      var meta_prop_value=get_meta.get_property_value();
      var th_width=(meta_name[p].length)*8;

      table_titles+='<th style="width:'+th_width+'px">'+meta_name[p]+'</th>';
      
      BOM_table_width+=th_width;
    }
  }
}



document.getElementById('BOM_Table_div').innerHTML=''
//+'<div style="width:300px;height:400px;background-color:green;"></div>'
+'<div id="table_container"><table id="BOM_Table">'
+table_titles
+'</table></div>'


var t=0
for (t = 0;t<=new_position-1;t++)
{
    var test_id=Part_Id_with_qtity[t]
    var test_id_pos=test_id.indexOf('#')
    if(test_id_pos>0)
    {
    test_id=test_id.substring(0,test_id_pos);
    }
    var choose_icon=myObject.IsPureAssy('<CLitSelection Name="">'+test_id+'</CLitSelection>')
    if(choose_icon==true)
    {
    var icon_path="resources/img/assy_icon.png"
    }
    else
    {
    var icon_path="resources/img/part_icon.png"
    }

    var myNewBomRow = document.getElementById('BOM_Table').insertRow(t+1);
    myNewBomRow.id='Row_'+Part_full_information[1][t]
    document.getElementById('Row_'+Part_full_information[1][t]).style.verticalAlign="middle"

      if(t%2==0)
      {
        $('#Row_'+Part_full_information[1][t]).addClass('bom_line_pair');    
      }
      else
      {
        $('#Row_'+Part_full_information[1][t]).addClass('bom_line_unpair');
      }

    var MyNewBomCell=myNewBomRow.insertCell(0);
    MyNewBomCell.id='Name_'+Part_full_information[1][t]
    MyNewBomCell.name='Name_'+Part_Id_with_qtity[t]
    document.getElementById('Name_'+Part_full_information[1][t]).innerHTML="<img src='"+icon_path+"' style='float:left;'> "+Part_full_information[0][t]
    document.getElementById('Name_'+Part_full_information[1][t]).style.verticalAlign="middle"

    
    var MyNewBomCell2=myNewBomRow.insertCell(1);
    MyNewBomCell2.id='Bom_'+Part_full_information[1][t]
    MyNewBomCell2.name='Bom_'+Part_Id_with_qtity[t]
    document.getElementById('Bom_'+Part_full_information[1][t]).innerHTML=Part_full_information[1][t]
    document.getElementById('Bom_'+Part_full_information[1][t]).style.verticalAlign="middle"
    
    var MyNewBomCell3=myNewBomRow.insertCell(2);
    MyNewBomCell3.id='Qtity_'+Part_full_information[1][t]
    MyNewBomCell3.name='Qtity_'+Part_Id_with_qtity[t]
    document.getElementById('Qtity_'+Part_full_information[1][t]).innerHTML=Part_full_information[2][t]
    document.getElementById('Qtity_'+Part_full_information[1][t]).style.verticalAlign="middle"
   
    myNewBomRow.onclick=function()
    {
    var rindex=this.rowIndex
    Show(Part_Id_with_qtity[rindex-1])
    }

    myNewBomRow.onmouseover=function()
    {
    var rindex = this.rowIndex
    Highlight(Part_Id_with_qtity[rindex - 1])
    $('#Row_'+Part_full_information[1][rindex-1]).addClass('bom_line_highlight');
    }    

    myNewBomRow.onmouseout=function()
    {
    var rindex=this.rowIndex
    $('#Row_'+Part_full_information[1][rindex-1]).removeClass('bom_line_highlight');
    } 

    if(add_meta=='yes')
    {
    var inc=1
    for (i = 1;i<=meta_name.length-1;i++)
      {
      if (document.getElementById(meta_name[i]).checked==true)
        { 
          var get_meta = new get_property('<CLitSelection Name="">'+test_id+'</CLitSelection>','Meta.'+meta_name[i]);
          var meta_prop_value=get_meta.get_property_value() 
  
          var j=2+inc
          var m=3+i;
          var cell_id="Meta_"+meta_name[i]+t
          //var cell_width=(meta_name[i].length)*8
          eval('var MyNewBomCell'+(m)+'=myNewBomRow.insertCell('+j+');')
          eval('MyNewBomCell'+(m)+'.id="'+cell_id+'";')
          //eval('MyNewBomCell'+(m)+'.style.width="'+cell_width+'px";')
          document.getElementById(cell_id).innerHTML="<span>"+meta_prop_value+"</span>"
          inc+=1;
        }
      }
    }    
   
}


document.getElementById('BOM_Table').style.width=BOM_table_width+'px';
//var bom_table_height=25+(18*t); //th + td_height*n
//document.getElementById('BOM_Table').style.height=bom_table_height+'px';


///////Removes the blue contour with assy selection//////////////////////
/*myObject.AssySelectionModeViewportIndicator(0);
myObject.ShowPaper(0);*/
       
/****************************************/ 

//$('#table_container').jScrollPane({showArrows:true,horizontalGutter:10});
}

var meta_first_open=0;
function Meta_win()
{

setBackgroundImage(myObject,"3D");

$('#meta_dialog').dialog('open')

if(meta_first_open==0)
{get_all_metas()}

meta_first_open+=1
}
////////This function allow sorting the BOM table.

function alpha_up(a,b)
  {
	var copyA=a+"";
	var copyB=b+"";
	return gather[++gather.length-1]=
	(copyA.toLowerCase()<copyB.toLowerCase())?-1:
	(copyA.toLowerCase()>copyB.toLowerCase())?1:0;
	}
function alpha_down(a,b)
  {
	var copyA=a+"";
	var copyB=b+"";
	return gather[++gather.length-1]=
  (copyA.toLowerCase()<copyB.toLowerCase())?1:
  (copyA.toLowerCase()>copyB.toLowerCase())?-1:0;
	}
function CompareNumeric_up(a, b)
  {
	var copyA=a+"";
	var copyB=b+"";
	return gather[++gather.length-1]=
  (isNaN(copyA))?0:
  (isNaN(copyB))?0:(copyA - copyB);
	}

function CompareNumeric_down(a, b)
  {
	var copyA=a+"";
	var copyB=b+"";
	return gather[++gather.length-1]=
  (isNaN(copyA))?0:
  (isNaN(copyB))?0:(copyB - copyA);
	}

var reverse_table=0
var gather
function multisort(arrayOfArrays,type)
{


if(!arrayOfArrays || typeof(arrayOfArrays)!="object"){return false;};
gather=[];
//Sort leading array only.

/////this 'if + else' is used to reverse the sorting
if ( (reverse_table%2) == 0) 
{
  if(type==1)
    {
    arrayOfArrays[0].sort(alpha_up);
    }
  if(type==2)
    {
    arrayOfArrays[0].sort(CompareNumeric_up);
    }
}
else
{
  if(type==1)
    {
    arrayOfArrays[0].sort(alpha_down);
    }
  if(type==2)
    {
    arrayOfArrays[0].sort(CompareNumeric_down);
    }
}


//Reorder other arrays:
for(var i=1; i<arrayOfArrays.length; i++){
var feedIterator=0;
arrayOfArrays[i].sort(
	function(a,b){
	return gather[feedIterator++];
	}
);
}

reverse_table=reverse_table+1
return arrayOfArrays;
}






//The Highlight function allows highlighting the part when the mouse is over a name in the BOM table


function Highlight(Id)
{
selected_from_BOM_highligh=1
var test_id=Id
var test_id_pos=test_id.indexOf('#')
if(test_id>0)
{test_id=test_id.substring(0,test_id_pos)}

var element_type=myObject.IsPureAssy('<CLitSelection Name="">'+test_id+'</CLitSelection>')

if(element_type==true)
{
myObject.AssySelectionMode=1;
}
else
{
myObject.AssySelectionMode=0;
}

myObject.Selection = '<CLitSelection Name="">' + Id + '</CLitSelection>';
selected_from_BOM_highligh=0
}

var collab_turned_off=0
function Show(Id)
{
if(is_3d_window==1) //if there is a detail view, this shows the detail in it. If not, this shows in the main scene.
{
  if(Id.indexOf("#")>0) //to see only one part if there are several instances.
  {
  Id=Id.substring(0,Id.indexOf("#"))
  }
  myObject2.SetVisibility('<CLitSelection Name="">'+Id+'</CLitSelection>',1,2) ;
  myObject2.ZoomFitAll();
}
else
{
  myObject.ZoomSelection();
}
collab_turned_off=collab_turned_off+1
}

var cell_id_cleans

var Select_name
var Select_name_old=""
var first_click=0
function select_in_table(selected_part)
{


if (myObject.AssySelectionMode==1)
{
    var Id_of_its_child=myObject.GetAssyChild(selected_part);
    var one_id_pos=Id_of_its_child.indexOf('>')
    var one_id_pos2=Id_of_its_child.indexOf('#')
    var one_id=Id_of_its_child.substring(one_id_pos+1,one_id_pos2)
    var prop_of_group=myObject.GetProperties('<CLitSelection Name="">'+one_id+'#</CLitSelection>',0,0)
    var group_name_pos=prop_of_group.indexOf("Actor.BomId");
    var prop_of_group=prop_of_group.slice(group_name_pos+1);
    var equal_pos2=prop_of_group.indexOf('=') ;
    var sup_pos2=prop_of_group.indexOf("/>") ;
    Select_name=prop_of_group.substring(equal_pos2+2,sup_pos2-1);
}
else
{
    var prop_of_group=myObject.GetProperties(selected_part,0,0) 
    var group_name_pos=prop_of_group.indexOf("Actor.BomId");
    var prop_of_group=prop_of_group.slice(group_name_pos+1);
    var equal_pos2=prop_of_group.indexOf('=') ;
    var sup_pos2=prop_of_group.indexOf("/>") ;
    Select_name=prop_of_group.substring(equal_pos2+2,sup_pos2-1);
}





var viewport_prop=myObject.GetViewport()
var select_prop=myObject.GetProperties(selected_part,0,0)


//Here is defined the color for the highlight in the table when a part is selected
if(viewport_prop==select_prop)
{
  if (first_click==0)
  {;}
  else
  {
  first_click=0
  document.getElementById('Name_'+Select_name_old).style.fontWeight="normal"
  document.getElementById('Name_'+Select_name_old).style.color="#000000"
  High_name_old=""
  }
}
else
{
  if (first_click>0)
  {
  document.getElementById('Name_'+Select_name_old).style.fontWeight="normal"

  document.getElementById('Name_'+Select_name).style.fontWeight="bold"

  
  }
  else
  {
  document.getElementById('Name_'+Select_name).style.fontWeight="bold"
  }
  location.hash='Name_'+Select_name;
  Select_name_old=Select_name;
  first_click=first_click+1;


}

select_to_highlight=0
}


var meta_value=new Array()
var meta_name=new Array()
var meta_definition;
function get_all_metas()
{
meta_number=0;

document.getElementById('meta_table').innerHTML=''
+'<table id="meta_rows_table">'
+'</table>'

var meta_def=myObject.GetAllMetaPropertyDefinitions()
var meta_def_array=meta_def.split("<Meta Name=")

  for(i=1;i<=meta_def_array.length-1;i++)
  {
  var pos1=meta_def_array[i].indexOf('DefaultLabel=')
  var pos2=meta_def_array[i].indexOf(' Mergeable')  

  meta_name[i]=meta_def_array[i].substring(pos1+14,pos2-1)

    var myNewBomRow = document.getElementById('meta_rows_table').insertRow(i-1);
  
    var MyNewBomCell=myNewBomRow.insertCell(0);
    MyNewBomCell.id='Check_'+meta_name[i]
    MyNewBomCell.name='Check_'+meta_name[i]
   
    document.getElementById('Check_'+meta_name[i]).innerHTML="<input type='checkbox' id='"+meta_name[i]+"'>"
  
  
    var MyNewBomCell=myNewBomRow.insertCell(1);
    MyNewBomCell.id='Meta__'+meta_name[i]
    MyNewBomCell.name='Meta__'+meta_name[i]
    document.getElementById('Meta__'+meta_name[i]).innerHTML=meta_name[i]
    document.getElementById('Meta__'+meta_name[i]).style.width="240px"  

  }

}
