var parts
var place_table=0


var Part_Ids_previous_view=new Array()
var real_part_number
var reverse_table=1
function Part_name_and_bom_extraction()
{
/////Compuation of the number of visible actors///////////////
document.ComposerWeb1.UseGUID(1);   // the part Id are taken inot account instead of their names
var all_actors_with_collabs=document.ComposerWeb1.GetAllActors(0);  //returns all visible actors, even the collabs

var pos1=all_actors_with_collabs.indexOf('>');
var all_actors_with_collabs_1=all_actors_with_collabs.slice(pos1+1);

var pos2=all_actors_with_collabs_1.indexOf('<');
var all_actors_with_collabs_2=all_actors_with_collabs_1.substring(0,pos2)


Actors_Ids = all_actors_with_collabs_2.split("#")   //creation of an array for the Ids of the parts
var actors_number=Actors_Ids.length-1




/////Calculation of the number of parts/////////////
var p
Number_of_parts=0
Part_data=new Array()
Part_name=new Array()
Part_bom=new Array()
Part_Ids=new Array()
real_part_number=0


  for (p = 0;p<=actors_number-1;p++)
  {
  var properties=document.ComposerWeb1.GetProperties('<CLitSelection Name="">'+Actors_Ids[p]+'#</CLitSelection>',0,0)
  var string_chordal=properties.indexOf("ChordalError")   //if the actor has a 'chordal error', it is a geometry. Otherwise , it is a collab
  
  
    if (string_chordal>0)
      {
      Number_of_parts=Number_of_parts+1  //this is a counter in order to know the number of parts visible in the scene
      Part_Ids[Number_of_parts-1]=Actors_Ids[p]  //this build an array containg only the Ids of the parts and not the collaboration tools
      
      //Changes the 'label linked to property' for each part in order to see the name of the group when the mouse is over a part
       document.ComposerWeb1.SetPropertyset('<CLitSelection Name="">'+ Part_Ids[Number_of_parts-1]+'</CLitSelection>','<CLitPropertySet><Actor.LinkedToolTipPropertyName Value="Meta.PartName"/></CLitPropertySet>') 
  
      
      //Part name extraction//
      var name_pos=properties.indexOf("Actor.Name");
      var substep=properties.slice(name_pos+1);
      var equal_pos=substep.indexOf('=') ;
      var sup_pos=substep.indexOf("/>") ;
      partname=substep.substring(equal_pos+2,sup_pos-1);
      
      //Bom  Id extraction//    
      var bom_pos=properties.indexOf("<Actor.BomId");
      var substep2=properties.slice(bom_pos);
      var equal_pos2=substep2.indexOf('=') ;
      var sup_pos2=substep2.indexOf("/>") ;
      BOMid=substep2.substring(equal_pos2+2,sup_pos2-1);
     
  
      Part_name[Number_of_parts-1]=partname
      Part_bom[Number_of_parts-1]=BOMid
      real_part_number=real_part_number+1
  /////////////////////////////////////////////////////////////////////    
      
    }
  }

}


var new_position
var group_of_the_part_Ids=new Array()
var group_Ids=new Array()
var group_names=new Array()
var group_of_the_part=new Array()
var group_of_the_part_Ids_with_qtity=new Array()
var number_of_p=0 
var number_of_parent=new Array()   
var new_number=0 
function Analyse_number_of_group()
{
new_number=0
var le=0
var ze=0
for (le = 0;le<=real_part_number-1;le++)
{
/////////parents

//Id
number_of_p=0
var assy_Id=document.ComposerWeb1.GetAssyParents('<CLitSelection Name="">'+Part_Ids[le]+'</CLitSelection>')
var assy_Id_pos=assy_Id.indexOf(">");
var assy_Id_pos1=assy_Id.indexOf("#");
group_of_the_part_Ids[le]=assy_Id.substring(assy_Id_pos+1,assy_Id_pos1)
var assy_Id1=group_of_the_part_Ids[le]


//name
var assy_name=document.ComposerWeb1.GetProperties('<CLitSelection Name="">'+assy_Id1+'#</CLitSelection>',0,0)
var assy_name_pos=assy_name.indexOf("Actor.Name Value");
var assy_name=assy_name.slice(assy_name_pos+1);
var equal_pos=assy_name.indexOf('=') ;
var sup_pos=assy_name.indexOf("/>") ;
group_of_the_part[le]=assy_name.substring(equal_pos+2,sup_pos-1); 
var assy_names=group_of_the_part[le]


  do
  {
  
  var duplicated_group=assy_names.indexOf('-bis')
  
  
  //parents of parents...of parents...of parents etc.
  
  //Id
  if (duplicated_group==(-1))
  {
  group_Ids[new_number]=assy_Id1
  //document.ComposerWeb1.RemoveActors('<CLitSelection Name="">'+assy_Id1+'</CLitSelection>') 
  }
  var assy_Id2=document.ComposerWeb1.GetAssyParents('<CLitSelection Name="">'+assy_Id1+'</CLitSelection>')
  var id_extract_pos=assy_Id2.indexOf('>')
  var id_extract_pos2=assy_Id2.indexOf('#')    
  var assy_Id3=assy_Id2.substring(id_extract_pos+1,id_extract_pos2)
  
  
  
  

  //name
  if (duplicated_group==(-1))
  {
  group_names[new_number]=assy_names
  }
  var assy_name2=document.ComposerWeb1.GetProperties('<CLitSelection Name="">'+assy_Id3+'#</CLitSelection>',0,0)
  var assy_name_pos=assy_name2.indexOf("Actor.Name Value");
  var assy_name2=assy_name2.slice(assy_name_pos+1);
  var equal_pos=assy_name2.indexOf('=') ;
  var sup_pos=assy_name2.indexOf("/>") ;
  assy_names=assy_name2.substring(equal_pos+2,sup_pos-1); 
  
  if (duplicated_group==(-1))
  {
  new_number=new_number+1
  }
  assy_Id1=assy_Id3
  number_of_p=number_of_p+1
  
  }
  while(assy_Id3 != (-1));
}


//number_of_parent[le]=number_of_p
}




function Analyse_quantity()
{

Analyse_number_of_group()


Part_name_with_qtity=new Array()
Part_Bom_with_qtity=new Array()
Part_qtity=new Array()
group_of_the_part_Ids_with_qtity=new Array()
Part_Id_with_qtity=new Array()
new_position=0


//This array is sorted twice in order to get a good order bewteen the name of the par's groupe and it's Id
var part_data_sorted=multisort(new Array(group_Ids,group_names),1)
var part_data_sorted=multisort(new Array(group_names,group_Ids),1)


// This is the routine that analyse if there are different group with the same name and computes the quantity.
var assembly_number=0
var Id_for_doubled_group_id=""
var de
for (de = 0;de<=new_number-1;de++)
{

if(part_data_sorted[1][de]==part_data_sorted[1][de+1])
{;}
else
{
  if(part_data_sorted[0][de]==part_data_sorted[0][de+1])
  {   
  assembly_number=assembly_number+1
  Id_for_doubled_group_id=part_data_sorted[1][de]+"#"+Id_for_doubled_group_id  //For the groups that have he same Bom id, a new variable is created. This variable is a concatenation of the ID of the groups that have the same Id  
  }
  else
  {
  // this create new arrays depending on the pre-existance of the Bom Id
    Part_name_with_qtity[new_position]=part_data_sorted[0][de]
    Part_qtity[new_position]=(assembly_number+1)
    group_of_the_part_Ids_with_qtity[new_position]=Id_for_doubled_group_id+part_data_sorted[1][de]
    assembly_number=0
    Id_for_doubled_group_id=""
    new_position=new_position+1
  }
}


//Id_for_doubled_BOM=part_data_sorted[4][de]+"#"+Id_for_doubled_BOM  //For the Part that have he same Bom id, a new variable is created. This variable is a concatenation of the ID of the part that have the same BOMId
//Id_for_doubled_group_id=part_data_sorted[1][de]+"#"+Id_for_doubled_group_id  //For the groups that have he same Bom id, a new variable is created. This variable is a concatenation of the ID of the groups that have the same Id  

}
Part_full_information=new Array(Part_name_with_qtity,Part_qtity,group_of_the_part_Ids_with_qtity)
}

//This function allows sorting the BOM table.

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


var gather
function multisort(arrayOfArrays,type){
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

//array_sorted=array_sorted+1

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


//Part_full_information=new Array(Part_name_with_qtity,Part_qtity,group_of_the_part_Ids_with_qtity)


function Build_Table()
{


document.getElementById('Parts_Catalogue').innerHTML='<table id="test" width="100%" align="left" border="0" cellspacing="1" cellpadding="1"></table>'
var t=0
for (t = 0;t<=new_position-1;t++)
{

    var myNewBomRow = document.getElementById("test").insertRow(t);
    var MyNewBomCell=myNewBomRow.insertCell(0);
    MyNewBomCell.id='Name_'+Part_full_information[0][t];
    MyNewBomCell.name='Name_'+Part_Id_with_qtity[t];
    //document.getElementById('Name_'+Part_full_information[0][t]).style.backgroundColor = "#F3F3F6";
    document.getElementById('Name_'+Part_full_information[0][t]).style.fontSize = "11px";  
    
    if (language=='FR')
    {
    document.getElementById('Name_'+Part_full_information[0][t]).innerHTML="<a id="+Part_full_information[0][t].replace(/ /g,'_')+" name="+Part_full_information[0][t].replace(/ /g,'_')+" onMouseOver=\"javascript:Highlight('"+Part_full_information[2][t]+"');\" onclick=\"javascript:Select('"+Part_full_information[2][t]+"');\">"+Part_full_information[0][t]+"</a>"
    }
    else
    {
    
    var meta_to_display=document.ComposerWeb1.GetPropertyValue('<CLitSelection>'+Part_full_information[2][t]+'</CLitSelection>',"Meta.English_Name")
    var metpos1=meta_to_display.indexOf("=")
    var metpos2=meta_to_display.indexOf("/>")
    
    meta_to_display=meta_to_display.substring(metpos1+2,metpos2-1)
    
    
    document.getElementById('Name_'+Part_full_information[0][t]).innerHTML="<a id="+Part_full_information[0][t].replace(/ /g,'_')+" name="+Part_full_information[0][t].replace(/ /g,'_')+" onMouseOver=\"javascript:Highlight('"+Part_full_information[2][t]+"');\" onclick=\"javascript:Select('"+Part_full_information[2][t]+"');\">"+meta_to_display+"</a>"    
    }
    
    //var MyNewBomCell3=myNewBomRow.insertCell(1);

    //MyNewBomCell3.id='Qtity_'+Part_full_information[0][t]
    //MyNewBomCell3.name='Qtity_'+Part_Id_with_qtity[t]
    //document.getElementById('Qtity_'+Part_full_information[0][t]).style.backgroundColor = "#F3F3F6";
    //document.getElementById('Qtity_'+Part_full_information[0][t]).style.fontSize = "10px";
    
    //this is done to adjust the quantity cells if the scroll bar is required
    //var number_of_row_visible_in_theBOM_table=16
    //if (new_position>number_of_row_visible_in_theBOM_table)
    //{
    //document.getElementById('Qtity_'+Part_full_information[0][t]).style.width = "85px";
    //}
    //else
    //{
    //document.getElementById('Qtity_'+Part_full_information[0][t]).style.width = "102px";
    //}
   // document.getElementById('Qtity_'+Part_full_information[0][t]).style.textAlign = "center";
    //document.getElementById('Qtity_'+Part_full_information[0][t]).innerHTML="<a onMouseOver=\"javascript:Highlight('"+Part_full_information[2][t]+"')\" onclick=javascript:Show('"+Part_full_information[2][t]+"');>"+Part_full_information[1][t]+"</a>"
     
    myNewBomRow.id='Row_'+Part_full_information[0][t].replace(/ /g,'_');
	//alert(myNewBomRow.id);
}
//$('.scroll-pane').jScrollPane({showArrows:true, animateTo:true, arrowSize: 16, scrollbarWidth:20, scrollbarMargin:10, reinitialiseOnImageLoad: true});


}

//The Highlight function allows highlighting the part when the mouse is over a name in the Delta BOM table
var select_to_highlight=0 
var select_to_highlight2=0
var not_shown_in_deatiled_view=0
function Highlight(Id)
{

not_shown_in_deatiled_view=1

select_to_highlight=select_to_highlight+1
select_to_highlight2=select_to_highlight2+1
document.ComposerWeb1.Selection('<CLitSelection>'+Id+'</CLitSelection>') ;
select_to_highlight=0

not_shown_in_deatiled_view=0

}

var parts_to_show=''
function Select(Id)
{
select_in_table('<CLitSelection Name="">'+Id+'</CLitSelection>')
Displayallmetas('<CLitSelection Name="">'+Id+'</CLitSelection>')


//Displayallmetas('<CLitSelection Name="">'+Id+'</CLitSelection>')
document.ComposerWeb1.Selection('<CLitSelection>'+Id+'</CLitSelection>') ;
document.ComposerWeb2.SetVisibility('<CLitSelection>'+Id+'</CLitSelection>',1,3)
document.ComposerWeb2.ZoomFitAll()
document.ComposerWeb2.RefreshScene(1)
}


function get_all_child_ids(assyid)
{
var child=document.ComposerWeb1.GetAssyChild('<CLitSelection Name="">'+assyid+'</CLitSelection>');
var supsignpos=child.indexOf('>')
var poundsignpos=child.lastIndexOf('#')
var group_of_child_id=child.substring(supsignpos+1,poundsignpos)
var childs_ids=group_of_child_id.split("#")
 
var childs_ids_length=childs_ids.length

var ft
for (ft = 0;ft<=(childs_ids_length-1);ft++)
{
  var is_assy=document.ComposerWeb1.IsPureAssy('<CLitSelection Name="">'+childs_ids[ft]+'</CLitSelection>') 

  
  if (is_assy==false)
  {
  parts_to_show=childs_ids[ft]+'#'+parts_to_show
  }
  else
  {
  get_all_child_ids(childs_ids[ft])
  }
}
}



////display meta properties////
var pp
function Displayallmetas(actor)
{

if(not_shown_in_deatiled_view!=1)
{
//document.getElementById('Buy_meta').style.display="block";
//If Assy mode is disabled, it it set back automatically
if (part_in_selection_mode>0)
{
actor=document.ComposerWeb1.GetAssyParents(actor)
part_in_selection_mode=0
}

document.getElementById('text_meta').innerHTML='<table id="meta_list_pella" border="0" cellspacing="4"></table>'   //clear the table

var allprop=document.ComposerWeb1.GetProperties(actor,0,0)


var tableformetas
var tableformeta=new Array()
tableformetas = allprop.split("Meta.") //displays all properites containing "meta"//


var size2=tableformetas.length
var qq=0
var ss
for (ss = 0;ss<=(size2-1);ss++)
{
  if(tableformetas[ss].indexOf("English")!=(-1))
  {;}
  else
  {
  tableformeta[qq]=tableformetas[ss]
  qq=qq+1
  }
}


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


myNewRowmeta1 = document.getElementById("meta_list_pella").insertRow(pp-1); //add a new line to the table each time

//name of meta//
myNewCellmeta1=myNewRowmeta1.insertCell(0)
myNewCellmeta1.id=metadef1
document.getElementById(myNewCellmeta1.id).width="150px"
document.getElementById(myNewCellmeta1.id).innerHTML="<b>"+metadef1+"<b>"

//value of meta//
myNewCellmeta2=myNewRowmeta1.insertCell(1)
myNewCellmeta2.id="value"+metadef1
document.getElementById(myNewCellmeta2.id).width="100%"
document.getElementById(myNewCellmeta2.id).innerHTML=metavalue



}

myNewRowmeta2 = document.getElementById("meta_list_pella").insertRow(4);

myNewCellmeta2_1=myNewRowmeta2.insertCell(0)
myNewCellmeta2_1.id="Quantity_cell"
document.getElementById(myNewCellmeta2_1.id).width="150px"
document.getElementById(myNewCellmeta2_1.id).innerHTML="<b>Quantite<b>"


myNewCellmeta2_2=myNewRowmeta2.insertCell(1)
myNewCellmeta2_2.id="Quantity_number"
document.getElementById(myNewCellmeta2_2.id).width="100%"
document.getElementById(myNewCellmeta2_2.id).innerHTML='<input type="text" name="nom" size="3">'




myNewRowmeta3 = document.getElementById("meta_list_pella").insertRow(5);

myNewCellmeta3_1=myNewRowmeta3.insertCell(0)
myNewCellmeta3_1.id="Button_cell"
document.getElementById(myNewCellmeta3_1.id).width="150px"
document.getElementById(myNewCellmeta3_1.id).innerHTML="<button type='button' name='cart_button' id='cart'>Add to Cart</button>"


myNewCellmeta3_2=myNewRowmeta3.insertCell(1)
myNewCellmeta3_2.id="Empty_cell"
document.getElementById(myNewCellmeta3_2.id).width="100%"
document.getElementById(myNewCellmeta3_2.id).innerHTML=""


}
//////////////////////////////////
}



var test_digger=0
function call_digger()

{

if (test_digger%2==0)
      {
      document.ComposerWeb1.SetDigger('<CLitPropertySet><Digger.COIOn Value="0"/><Digger.COIPos X="0.000000" Y="0.000000" Z="0.000000"/><Digger.Position X="0.522000" Y="0.503731" Z="0.000000"/><Digger.Radius Value="0,150"/><Digger.Renderer Value="3"/><Inspector.Enabled Value="1"/></CLitPropertySet>')
      document.ComposerWeb1.RefreshScene(1) 
      test_digger=test_digger+1
      }
else
    {
      document.ComposerWeb1.SetDigger('<CLitPropertySet><Digger.COIOn Value="0"/><Digger.COIPos X="0.000000" Y="0.000000" Z="0.000000"/><Digger.Position X="0.522000" Y="0.503731" Z="0.000000"/><Digger.Radius Value="0,150"/><Digger.Renderer Value="3"/><Inspector.Enabled Value="0"/></CLitPropertySet>')
      document.ComposerWeb1.RefreshScene(1)  
      test_digger=test_digger+1    
    } 
}


var cell_id_cleans
var test
var testId=0
var High_name
function Highlight3DToTable(part)
{
    var Id_of_its_parent=document.ComposerWeb1.GetAssyParents(part);
    var prop_of_group=document.ComposerWeb1.GetProperties(Id_of_its_parent,0,0) 
    var group_name_pos=prop_of_group.indexOf("Actor.Name");
    var prop_of_group=prop_of_group.slice(group_name_pos+1);
    var equal_pos2=prop_of_group.indexOf('=') ;
    var sup_pos2=prop_of_group.indexOf("/>") ;
    High_name=prop_of_group.substring(equal_pos2+2,sup_pos2-1);
    

var is_there_a_bis=High_name.indexOf('-bis')
if (is_there_a_bis!=(-1))
{
High_name=High_name.substring(0,is_there_a_bis)
}


    //document.getElementById('Name_'+High_name).style.backgroundColor = "#EEE8AA";
    //document.getElementById('Qtity_'+High_name).style.backgroundColor = "#dde0e6";

}


function Highlight3DToTreeOff()
{

  //document.getElementById('Name_'+High_name).style.backgroundColor = "#F3F3F6";
  //document.getElementById('Qtity_'+High_name).style.backgroundColor = "#F3F3F6";

}

var Select_name
var Select_name_old=""
var first_click=0
function select_in_table(selected_part)
{


//If Assy mode is disabled, it it set back automatically
if (part_in_selection_mode>0)
{
selected_part=document.ComposerWeb1.GetAssyParents(selected_part)
part_in_selection_mode=0
}

if(select_to_highlight>0)
{;}
else
{
var prop_of_group=document.ComposerWeb1.GetProperties(selected_part,0,0) 
var group_name_pos=prop_of_group.indexOf("Actor.Name");
var prop_of_group=prop_of_group.slice(group_name_pos+1);
var equal_pos2=prop_of_group.indexOf('=') ;
var sup_pos2=prop_of_group.indexOf("/>") ;
Select_name=prop_of_group.substring(equal_pos2+2,sup_pos2-1);


var is_there_a_bis=Select_name.indexOf('-bis')
if (is_there_a_bis!=(-1))
{
Select_name=Select_name.substring(0,is_there_a_bis);
}
//Select_name= Select_name.replace(/ /g,'_');
//alert (Select_name);
var viewport_prop=document.ComposerWeb1.GetViewport()
var select_prop=document.ComposerWeb1.GetProperties(selected_part,0,0)


//Here is defined the color for the highlight in the table when a part is selected
if(viewport_prop==select_prop)
{
  if (first_click==0)
  {;}
  else
  {
  first_click=0
  document.getElementById('Name_'+Select_name_old).style.fontWeight="normal"
  //document.getElementById('Qtity_'+Select_name_old).style.fontWeight="normal"
  //document.getElementById('Name_'+Select_name_old).style.color="#000000"
  //document.getElementById('Qtity_'+Select_name_old).style.color="#000000"
  High_name_old=""
  }
}
else
{
  if (first_click>0)
  {
  document.getElementById('Name_'+Select_name_old).style.fontWeight="normal"
  //document.getElementById('Qtity_'+Select_name_old).style.fontWeight="normal"
  //document.getElementById('Name_'+Select_name_old).style.color="#000000"
  //document.getElementById('Qtity_'+Select_name_old).style.color="#000000"
  
  //document.getElementById('Name_'+Select_name).style.color="#0094FF"
  //document.getElementById('Qtity_'+Select_name).style.color="#0094FF"
  document.getElementById('Name_'+Select_name).style.fontWeight="bold"
  //document.getElementById('Qtity_'+Select_name).style.fontWeight="bold"
  
  }
  else
  {
  document.getElementById('Name_'+Select_name).style.fontWeight="bold"
  //document.getElementById('Qtity_'+Select_name).style.fontWeight="bold"
  //document.getElementById('Name_'+Select_name).style.color="#0094FF"
  //document.getElementById('Qtity_'+Select_name).style.color="#0094FF"
  
  }
  
  // scrolling chris machin truc
  if(place_table==1)
  {//location.hash='Name_'+Select_name;
//$('.scroll-pane').jScrollPane({showArrows:true, arrowSize: 16, scrollbarWidth:20, scrollbarMargin:10, reinitialiseOnImageLoad: true});
	var $table_content2 = $('#table_content2');
	Select_name2= Select_name.replace(/ /g,'_');
	var targetElementSelectorString = '#Row_'+Select_name2;
	//alert(targetElementSelectorString);
	$table_content2[0].scrollTo(targetElementSelectorString);
}


  Select_name_old=Select_name;
  first_click=first_click+1;


}
}
select_to_highlight=0
}



var part_in_selection_mode=0
function turn_on_assy_mode(selected_part)
{

var is_that_an_assy=document.ComposerWeb1.IsPureAssy(selected_part)
if(is_that_an_assy==true)
{;}
else
{
document.ComposerWeb1.AssySelectionMode(1);
part_in_selection_mode=part_in_selection_mode+1
}


}


//Enable this function if the ActiveX version is Higher than 4.3
function version_higher_than_four_three()
{
//document.ComposerWeb1.ShowViewBar(0);
}

function showall()
{
document.ComposerWeb1.UseGUID(1);
var selection=document.ComposerWeb1.GetAllActors(0);
document.ComposerWeb1.setvisibility(selection,1,1);
document.ComposerWeb1.ZoomFitAll();
var collab=document.ComposerWeb1.GetAllCollaborations()
document.ComposerWeb1.setvisibility(collab,2,0);
document.ComposerWeb1.RefreshScene(1);
}



function popup()
{
window.open ('Buy_it.html', 'Message', config='height=300, width=400, toolbar=no, menubar=no, scrollbars=no, resizable=no, location=no, directories=no, status=no')
}



function display_validate(div_id,div2_id)
{

if(document.getElementById(div_id).src=="images/radio_off.gif")
{;}
else
{
document.getElementById(div_id).src="images/radio_on.gif"
document.getElementById(div2_id).src="images/radio_off.gif"
}
document.ComposerWeb1.GoToConfiguration(div_id);
document.ComposerWeb1.RefreshScene(1);
}

function display_validate2(div_id,div2_id)
{

if(document.getElementById(div_id).src=="images/radio_off.gif")
{;}
else
{
document.getElementById(div_id).src="images/radio_on.gif"
document.getElementById(div2_id).src="images/radio_off.gif"
}
document.ComposerWeb1.GoToConfiguration(div_id);
document.ComposerWeb1.RefreshScene(1);
}

function Color(Conf_Color)
{
document.ComposerWeb1.GoToConfiguration(Conf_Color);
document.ComposerWeb1.RefreshScene(1);
}


function Switch_div()
{

if(document.getElementById('Config_div').style.display=="none")
{ 
  document.getElementById('Part_List_div').style.display="none";
  document.getElementById('Config_div').style.display="block";
  
  document.getElementById('conf_left_corner').src="images/label_left_corner.jpg";
  document.getElementById('conf_right_corner').src="images/label_right_corner.jpg";
  //document.getElementById('Conf_tab').style.backgroundColor="#B6B6B6";
  
  document.getElementById('part_left_corner').src="images/label_fill.jpg";
  document.getElementById('part_right_corner').src="images/label_fill.jpg";
  //document.getElementById('Part_tab').style.backgroundColor="#969696"  
}

}

function Switch_div2()
{

if(document.getElementById('Part_List_div').style.display=="none")
{ 
  document.getElementById('Config_div').style.display="none";
  document.getElementById('Part_List_div').style.display="block";

  document.getElementById('part_left_corner').src="images/label_left_corner.jpg";
  document.getElementById('part_right_corner').src="images/label_right_corner.jpg";
  //document.getElementById('Part_tab').style.backgroundColor="#B6B6B6";
  
  document.getElementById('conf_left_corner').src="images/label_fill.jpg";
  document.getElementById('conf_right_corner').src="images/label_fill.jpg";
  //document.getElementById('Conf_tab').style.backgroundColor="#969696";  

}

}


function Orange_Ball(pic_div)
{
var radio_path=document.getElementById(pic_div).src
var radio_state_pos=radio_path.lastIndexOf('/');
var radio_state=radio_path.substring(radio_state_pos+1,radio_path.length)

if(radio_state=="radio_off.gif")
  {
  document.getElementById(pic_div).src="images/radio_rollover.gif";
  }
}

function Grey_Ball(pic_div2)
{
var radio_path2=document.getElementById(pic_div2).src
var radio_state_pos2=radio_path2.lastIndexOf('/');
var radio_state2=radio_path2.substring(radio_state_pos2+1,radio_path2.length)
//alert(radio_state2)
if(radio_state2=="radio_rollover.gif")
  {
  document.getElementById(pic_div2).src="images/radio_off.gif";
  }
}

var language='FR'
function Switch_French() 
{
    var aryClassElements1 = getElementsByClassName( 'French', document.body );
    var aryClassElements2 = getElementsByClassName( 'English', document.body );
    for ( var i = 0; i < aryClassElements1.length; i++ ) {
        aryClassElements1[i].style.display="block";
        aryClassElements2[i].style.display="none";
    }

language='FR'   
Build_Table();
}


function Switch_English() 
{
    var aryClassElements1 = getElementsByClassName( 'French', document.body );
    var aryClassElements2 = getElementsByClassName( 'English', document.body );
    for ( var i = 0; i < aryClassElements1.length; i++ ) {
        aryClassElements1[i].style.display="none";
        aryClassElements2[i].style.display="block";
    }
    
language='ENG'    
Build_Table();
    
}



function getElementsByClassName( strClassName, obj ) {
    var ar = arguments[2] || new Array();
    var re = new RegExp("\\b" + strClassName + "\\b", "g");

    if ( re.test(obj.className) ) {
        ar.push( obj );
    }
    for ( var i = 0; i < obj.childNodes.length; i++ )
        getElementsByClassName( strClassName, obj.childNodes[i], ar );
    
    return ar;
}


