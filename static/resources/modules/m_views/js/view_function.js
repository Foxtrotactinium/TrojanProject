// JavaScript Document

var view_list
var view= new Array()
var view_id= new Array()
function Build_Views_Pane(views_name,views_id)
{
myObject.ShowPaper = 0;
/////////Create an array containg the name of the Views
////////////but the name is not isaloted yet//////////
views_name=views_name.split('CLitModifiable')

var pos1=views_id.indexOf('>')
var pos2=views_id.lastIndexOf('#<')

views_id=views_id.substring(pos1+1,pos2)
view_id=views_id.split('#')

///////loop to isolate the view name
for (i = 1;i<=views_name.length-1;i++) 
{
var equal_position=views_name[i].indexOf('=')
var sign_position=views_name[i].indexOf('/>')

view[i-1]=views_name[i].substring(equal_position+2,sign_position-1)
}

//////Creates the table that will containthe views//////
//var table_for_views='<table id="View_List_table" border="0" cellspacing="0" cellpadding="0"></table>'
//document.getElementById('View_Zone').innerHTML=table_for_views
var smg_path=myObject.FileName;

if (file_opened_from_button==0)
{
var pos1=smg_path.lastIndexOf('\\')
var smg_name=smg_path.slice(pos1+1)
var pos2=smg_name.lastIndexOf('.')
smg_name=smg_name.substring(0,pos2)
smg_name=smg_name+"_files"
}

else 
{
    // Logic to find current folder in case of different file formats as per Composer.
    // For smgXml we read from the same folder where .smgXml file is present.
    // For smgProj we'll always have a folder with same name as filename in the same folder where .smgProj file is present.
    // For smg we unzip it in temp folder of Appdata and refer all the inputs from there.
    var pos1 = smg_path.lastIndexOf('\\');
    var pos2 = smg_path.lastIndexOf('.');
    var ext = smg_path.substring(pos2 + 1).toLowerCase();
    if (ext == "smgxml") {
        smg_name = "file:///" + smg_path.substring(0, pos1);
    }
    else if (ext == "smgproj") {
        smg_name = "file:///" + smg_path.substring(0, pos2);
    }
    else {
        var filename = smg_path.substring(pos1+1, pos2);
        smg_name = "file:///" + myObject.GetTempFolder() + "DSComposerWork\\" + filename;
    }
}

document.getElementById('View_Zone').innerHTML=""

////loop to write the view in the View table////
for (k = 0;k<=view.length-1;k++) 
{

var View_card=''
  +'<div class="ui-widget-content2">'
  +"<img width='90%' height='65%' src='"+smg_name+"/View"+view_id[k]+".jpg' onclick='Javascript:Launch_View(\""+view_id[k]+"\")'/>"
  +'<h5 class="ui-widget-header2" id="alb_title_'+k+'"><table class="h5_title" style="height:28px;"><tr><td>'+view[k]+'</td></tr></table></h5>'
  +'</div>'

$('#View_Zone').append(View_card)


}
//$('#View_Zone').jScrollPane({showArrows:true,horizontalGutter:10});
}

function Launch_View(view_to_launch)
{
myObject.GoToView(view_to_launch)
if(is_bom==1)
{
init_BOM()
}
}
