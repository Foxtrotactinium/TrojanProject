/*****global variable*///////
var current_select_mode
var selected_from_tree_highligh=0 
var selected_from_BOM_highligh = 0
var expand_tree = 0
/**************************/ 

function Show_Help()
{
setBackgroundImage(myObject, "3D");
 
$('#dialog_help').dialog('open')
}

function Show_App_prop()
{
setBackgroundImage(myObject,"3D");
  
var is_ground=myObject.GroundGrid;
  if(is_ground==true)
  {
  document.getElementById('Ground_box').checked=true
  }

var is_shadow=myObject.RenderGroundShadow;
  if(is_shadow==true)
  {
  document.getElementById('Shadow_box').checked=true
  }

if(is_playerpro==false)
{
  document.getElementById('main_backgrd_color').style.display="none";
}

$('#App_prop').dialog('open')
}

//This is to set the selection mode back to its orginal state even if it has been changed with highlight on the tree or in the BOM
function get_select_mode()
{
current_select_mode=myObject.AssySelectionMode;
}

function set_select_mode()
{
selected_from_tree_highligh=1;
myObject.AssySelectionMode=current_select_mode;
selected_from_tree_highligh=0;
}

function Show_Hide_detail_view()
{
var detail_view_box_state=document.getElementById('detail_view_box').checked
if(detail_view_box_state==true)
{
    document.getElementById('draggable_detail_view').style.visibility = "visible";
    myObject2.style.visibility = "visible";
    is_3d_window=1;
}
else
{
    document.getElementById('draggable_detail_view').style.visibility = "hidden";
    myObject2.style.visibility = "hidden";
    is_3d_window=0;
}

}
/////////////////////////////////////////////////////////////////////////////////// 


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


function Trigger_OnchangeSelection(part_selection)
{
  if (is_playerpro==true)
  {
    //var is_viewport=myObject.GetPropertyValue(part_selection,"Viewport.Bk.Alpha")
    
    //if(is_viewport.length==20)
    //Commented the above code. The behaviour of the method (GetPropertyValue) has been changed (IR-380283) and we no longer need to use it in the above way

    {
      /*if(is_meta==1)
      {
      Displayallmetas(part_selection)
      }*/
      //alert(selected_from_BOM_highligh)
      if (is_tree == 1 && expand_tree == 1 /*&& selected_from_tree_highligh == 0 && selected_from_BOM_highligh == 0*/)
      {
    
          /************************To select in the tree*****************************/
            var is_pure_Assy=myObject.IsPureAssy(part_selection)
           
              var selected_part_id 
              var pos1=part_selection.indexOf('>');
              part_selection=part_selection.slice(pos1+1);
              var pos2=part_selection.indexOf('#<');
              selected_part_id=part_selection.substring(0,pos2); 
           
        if(document.getElementById('Tree_name'+selected_part_id))
        {        
            if(is_pure_Assy==false)
            {var select_tree_color="#FF8000"}
            else
            {var select_tree_color="#0080FF"}
          
            document.getElementById('Tree_name'+selected_part_id).style.color=select_tree_color
            document.getElementById('Tree_name'+selected_part_id).style.fontWeight="bolder"
            
            if(old_id_to_select!='')
            {
              document.getElementById('Tree_name'+old_id_to_select).style.color="black"
              document.getElementById('Tree_name'+old_id_to_select).style.fontWeight="normal"
            }
             old_id_to_select=selected_part_id
          /*****************************************************/
          
          /************************To open the eye*****************************/  
        
          var Id_to_open_eye=selected_part_id
          do
          {
        
            if (document.getElementById(Id_to_open_eye))
            {open_eye(Id_to_open_eye,'eye_'+Id_to_open_eye,'from_3D')}
            var dot_pos=Id_to_open_eye.lastIndexOf('.')
            Id_to_open_eye=Id_to_open_eye.substring(0,dot_pos)
          }
          while(Id_to_open_eye.indexOf('.')!=-1)
          open_eye(Id_to_open_eye,'eye_'+Id_to_open_eye,'from_3D')
            
          /*****************************************************/
          
          }
    
        }
          selected_from_tree_highligh=0 
        
    }
  }
}


function Trigger_OnchangeHighlightOn(part_highlight)
{
  if (is_playerpro==true)
  {
    var is_collab=myObject.IsCollaboration(part_highlight)
    
    if(is_bom==1 && is_collab==false)
    {
        var get_BOMid = new get_property(part_highlight,"Actor.BomId");
        highligh_Bomid=get_BOMid.get_property_value()   
        if (document.getElementById('Row_'+highligh_Bomid))
        {    $('#Row_'+highligh_Bomid).addClass('bom_line_highlight');}
    }
  }
}

function Trigger_OnchangeHighlightOff(part_offhighlight)
{
  if (is_playerpro==true)
  {  
    var is_collab=myObject.IsCollaboration(part_offhighlight)
    
    if(is_bom==1 && is_collab==false)
    {
        var get_BOMid = new get_property(part_offhighlight,"Actor.BomId");
        highligh_Bomid=get_BOMid.get_property_value()   
        
        if (document.getElementById('Row_'+highligh_Bomid))
        {$('#Row_'+highligh_Bomid).removeClass('bom_line_highlight');}
    }
  }
}

function Trigger_OnEndLoadModel2()
{
  myObject2.ShowPaper = 0;
  if (is_playerpro==true)
  {
  var compass='<CLitSelection Name=""><CLitModifiable Name="Compass"/></CLitSelection>'
  myObject2.SetVisibility(compass,2,0)
  myObject2.RefreshScene(1)
  
  var collabs=myObject2.GetAllCollaborations()
  myObject2.SetVisibility('<CLitSelection Name="">'+collabs+'</CLitSelection>',2,0) ;
  
  //////this inits the properties pane
  if(is_pmi==1){document.getElementById('PMI_colors_option').style.display='block';}   
  if(is_3d_window==1)
    {
    document.getElementById('detail_window_prop').style.display='block';
    document.getElementById('detail_view').style.display='block';
    } 
  ///////////////////heck to avoid issue with magnet bar enabled///////////////////
  $('#dialog_detail_view').css('filter','')
  }
}


function Trigger_OnEndLoadModel()
{
	
myObject.AssySelectionModeViewportIndicator = 0;
myObject.ShowPaper = 0;

}


   
var test_digger=0
function call_digger()
{
if (test_digger%2==0)
      {
      myObject.SetDigger('<CLitPropertySet><Digger.COIOn Value="0"/><Digger.COIPos X="0.000000" Y="0.000000" Z="0.000000"/><Digger.Position X="0.522000" Y="0.503731" Z="0.000000"/><Digger.Radius Value="0,150"/><Digger.Renderer Value="3"/><Inspector.Enabled Value="1"/></CLitPropertySet>')
      myObject.RefreshScene(1) 
      test_digger=test_digger+1
      }
else
    {
      myObject.SetDigger('<CLitPropertySet><Digger.COIOn Value="0"/><Digger.COIPos X="0.000000" Y="0.000000" Z="0.000000"/><Digger.Position X="0.522000" Y="0.503731" Z="0.000000"/><Digger.Radius Value="0,150"/><Digger.Renderer Value="3"/><Inspector.Enabled Value="0"/></CLitPropertySet>')
      myObject.RefreshScene(1)  
      test_digger=test_digger+1    
    } 
}

function showall()
{
myObject.UseGUID = 1;
var selection=myObject.GetAllActors(0);
myObject.SetVisibility(selection,1,1);
myObject.ZoomFitAll();
var collab=myObject.GetAllCollaborations()
myObject.SetVisibility(collab,2,0);
myObject.RefreshScene(1);
}

var resizeDelay;
function Is_Resized()
{
  if (is_tree==1)
  {
    clearTimeout(resizeDelay);
    resizeDelay=setTimeout("reset_scroll()", 200);
  }
}    
 
var is_scroll_val=false;
function reset_scroll()
{
//api.getContentPane()  
api.reinitialise()
is_scroll =api.getIsScrollableV()
 
if(is_scroll==false)                      
{
$('#assembly_tree').parent().css('top', '0px');
//pane_to_scroll.style.top="0px";
}
}        

function ShowToolbar()
{      
myObject.ShowStandardToolBar=myObject.ShowStandardToolBar=="0"?"1":"0";
}

//function Load_3D()
//{
//document.getElementById('Open_3D_button').click() 
//}

var smg_path
var file_opened_from_button=0;
function File_3D_path()
{

//smg_path=document.getElementById('Open_3D_button').value
smg_path = myObject.FileBrowseDialog();
if (smg_path != "")
    myObject.FileName = smg_path;

/*
  if(is_3d_window==1)
  {
    myObject2.FileName(smg_path)
  }*/
file_opened_from_button=1;  
}
