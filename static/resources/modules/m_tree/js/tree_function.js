var part_prop
var meta_index
var meta_color
var meta_index_red
var meta_index_blue


var partid
var viewport_id
var model_structure=new Array()
var reverse_table=0

var visibility_state=1 
var t=0
var Actors_structure_Id=new Array()
var Actors_structure_Name=new Array()
var Actors_path=new Array()
var Actors_level=new Array()
var Actors_path_Id=new Array()
//var actorname
var actornamenext
var Actors_path_Id_next


var Select_name
var Select_name_old=""
var first_click=0

var assembly_tree="";

var has_meta="";
function Build_assembly_tree(Actor_Id,actorname_old,Actor_Id_old)
{

  var root = "";
  var background_url = "resources/img/dots.gif";

  if (Actor_Id == "")
  {
      root = myObject.GetAssyRoot();
      var root_pos1 = root.indexOf('>');
      root = root.slice(root_pos1 + 1);
      var root_pos2 = root.indexOf('#<');
      root = root.substring(0, root_pos2);
      var root_ids_intermediate = root.split("#"); 
      var root_ids=new Array()
      var f=0;
      
      for (j = 0;j<=(root_ids_intermediate.length - 1);j++)
      {
      
        var test_collab = myObject.IsCollaboration('<CLitSelection Name="">' + root_ids_intermediate[j] + '</CLitSelection>');
       
        if (test_collab == false)
        {
         root_ids[f]=root_ids_intermediate[j]
         f+=1; 
        }
         
      }       
                 
  }
  else
  {
      root = myObject.GetAssyChild('<CLitSelection Name="">' + Actor_Id + '</CLitSelection>');
      var root_pos1 = root.indexOf('>');
      root = root.slice(root_pos1 + 1);
      var root_pos2 = root.indexOf('#<');
      root = root.substring(0, root_pos2);
      var root_ids = root.split("#");  
  }






  var number_of_child_in_root = root_ids.length;
  var root_child_ids = new Array()
  var root_child_number = 0
  var s = 0
  var i = 0;

  var Child_Actor = '';
  var actorname = '';
  var actornamenext = '';
  

for (i = 0;i<=(number_of_child_in_root - 1);i++)
{

  Child_Actor = root_ids[i]; 

  var test_collab = myObject.IsCollaboration('<CLitSelection Name="">' + Child_Actor + '</CLitSelection>');
  if (test_collab == false)
  {

  var properties=myObject.GetProperties('<CLitSelection Name="">'+Child_Actor+'#</CLitSelection>',0,0)
  var has_child=myObject.HasChilds('<CLitSelection Name="">'+Child_Actor+'</CLitSelection>') 
  var is_pure_Assy=myObject.IsPureAssy('<CLitSelection Name="">'+Child_Actor+'</CLitSelection>')   

  ////Meta check
  var width_for_meta=0
  if(is_meta==1)
  {
    if (properties.indexOf('Meta.')>0)
    {has_meta='meta';width_for_meta=25;}
    else
    {has_meta='';width_for_meta=0;}
  }
  
  //Part name extraction//
  var name_pos=properties.indexOf("Actor.Name");
   
  if(name_pos>0)
  {  
  var substep=properties.slice(name_pos+1);
  var equal_pos=substep.indexOf('=') ;
  var sup_pos=substep.indexOf("/>") ;
  var actorname=substep.substring(equal_pos+2,sup_pos-1);  
  }
  else //this is done for views in the assembly tree
  {
  var last_pos=Child_Actor.lastIndexOf('.')
  actorname=Child_Actor.substring(last_pos+2,Child_Actor.length);
  }
  
  //////Actor ID
    Actors_structure_Id[t]=Child_Actor
  //////Actor name
    Actors_structure_Name[t]=actorname  
  //////Actor Path
    Actors_path[t]=actorname_old+actorname
    actornamenext=actorname_old+actorname+'§'
  //////Actor path in ID
  Actors_path_Id[t]=Actor_Id_old+Child_Actor
  Actors_path_Id_next=Actor_Id_old+Child_Actor+'§'
 
  t = t + 1;
 
/**********************icon definition*************************/    
    var icon_image;
    var eye_image;
    var background_url="";
    
    if(is_pure_Assy==true)
    {
      icon_image="resources/img/assy_icon.png"
      
      if (has_child==false)
      {eye_image="resources/img/doc.gif"}
      else
      { 
        if(i==(number_of_child_in_root-1))
        {
        eye_image="resources/img/closed_end.gif";
        background_url=""
        }
        else
        {
        eye_image="resources/img/closed.gif"
        background_url="resources/img/dots.gif"        
        }
      }
    }
    else
    {
      icon_image="resources/img/part_icon.png"
      if(i==(number_of_child_in_root-1))
      {eye_image="resources/img/doc_end.gif"}
      else
      {eye_image="resources/img/doc.gif"}
    }
    

/*************************************************************/    
    var element_length=actorname.length;
    //alert(width_for_meta)
    var element_width=(element_length*8)+50+width_for_meta ; //6px per letter + images size +width if meta
    
    
    
    
    //alert(element_width)
    assembly_tree+=''
                  +'<div class="tree_element" style="width:'+element_width+'px">'
                    +'<div style="display:inline;">'
                      +'<div style="float:left;">'
                        +'<img height="16" width="16" class="dot_cross" id="eye_'+Child_Actor+'" onclick="Javascript:open_eye(\''+Child_Actor+'\',\'eye_'+Child_Actor+'\',\'tree\')" src="'+eye_image+'" />'
                        +'<img height="16" width="16" class="eye" id="Img_'+Child_Actor+'" onclick="Javascript:Show_Hide_part(\''+Child_Actor+'\');" src="resources/img/eye1.gif" />'
                        +'<img height="16" width="16" src="'+icon_image+'"  class="icon_type" />'
                      +'</div>'
                      +'<div id="Tree_name'+Child_Actor+'" style="height:10px;margin-left:2px;top:0px;float:left;cursor:pointer;"'
                      +' onclick="Javascript:Select_element(\''+Child_Actor+'\');" '
                      +' onmouseover="Javascript:Tree_highligh(\''+Child_Actor+'\');" >'+actorname+'<span id="meta_sup'+Child_Actor+'"><sup> '+has_meta+'</sup></span></div>'
                    +'</div>'
                  +'</div>';  
      

      
      if (has_child==false)
      {
      }
      else
      { 
        
        assembly_tree+='<div class="div_block" style="display:none;background-image:url('+background_url+');padding-left:19px;" id="'+Child_Actor+'">';

        Build_assembly_tree(Child_Actor,actornamenext,Actors_path_Id_next);  
        assembly_tree+='</div>'      
      }
      
     
      
      /***********for the last child, this should close the container div********/
      //if(i==(number_of_child_in_root-1))
      //{assembly_tree+='</div>'}
    }

}

}


function Tree_highligh(Id)
{ 
selected_from_tree_highligh=1
var element_type=myObject.IsPureAssy('<CLitSelection Name="">'+Id+'</CLitSelection>')
  
  
  if(element_type==true)
  {
  myObject.AssySelectionMode=1;
  }
  else
  {
  myObject.AssySelectionMode=0;
  }
  
  myObject.Selection = '<CLitSelection Name="">'+Id+'</CLitSelection>';  

  if(is_meta==1)
  {
  Displayallmetas('<CLitSelection Name="">'+Id+'</CLitSelection>')
  }

}

var old_id_to_select=''
function Select_element(part_id)
{

  var is_pure_Assy=myObject.IsPureAssy('<CLitSelection Name="">'+part_id+'</CLitSelection>')
  
  if(is_pure_Assy==false)
  {var select_tree_color="#FF8000"}
  else
  {var select_tree_color="#0080FF"}

document.getElementById('Tree_name'+part_id).style.color=select_tree_color
document.getElementById('Tree_name'+part_id).style.fontWeight="bolder"

if(old_id_to_select!='')
{
document.getElementById('Tree_name'+old_id_to_select).style.color="black"
document.getElementById('Tree_name'+old_id_to_select).style.fontWeight="normal"
}

if(is_3d_window==1)
{
  myObject2.SetVisibility('<CLitSelection Name="">'+part_id+'</CLitSelection>',1,2);
  myObject2.ZoomFitAll();
}
else
{
  myObject.ZoomSelection();
}
old_id_to_select=part_id
}


function Show_Hide_part(part_id)
{

objImg3 = document.getElementById('Img_'+part_id);
if(objImg3.src.indexOf('resources/img/eye2.gif')>-1)
{
document.getElementById('Img_'+part_id).src="resources/img/eye1.gif";
myObject.SetVisibility('<CLitSelection Name="">'+part_id+'#</CLitSelection>',1,0)
}
else
{
document.getElementById('Img_'+part_id).src="resources/img/eye2.gif";
myObject.SetVisibility('<CLitSelection Name="">'+part_id+'#</CLitSelection>',2,0)
}



}



var openImg = new Image();
openImg.src = "resources/img/opened.gif";
var closedImg = new Image();
closedImg.src = "resources/img/closed.gif";
function open_eye(eye_id,Img_Id,from)
{

var img_src=document.getElementById(Img_Id).src

//objImg = document.getElementById(Img_Id);
if(img_src.indexOf('resources/img/closed.gif')>-1)
{
document.getElementById(Img_Id).src="resources/img/opened.gif";
document.getElementById(eye_id).style.display="block"
}
if(img_src.indexOf('resources/img/closed_end.gif')>-1)
{
document.getElementById(Img_Id).src="resources/img/opened_end.gif";
document.getElementById(eye_id).style.display="block"
}

if(from=='tree')
{
  if(img_src.indexOf('resources/img/opened_end.gif')>-1)
  {
  document.getElementById(Img_Id).src="resources/img/closed_end.gif";
  document.getElementById(eye_id).style.display="none"
  }
  if(img_src.indexOf('resources/img/opened.gif')>-1)
  {
  document.getElementById(Img_Id).src="resources/img/closed.gif";
  document.getElementById(eye_id).style.display="none"
  }
}
setTimeout("reset_scroll()",200);

}

