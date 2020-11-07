// JavaScript Document
function bckgrd_color_change(R,G,B)
{
var background_color='<CLitPropertySet><Viewport.Bk.Color R="'+R+'" G="'+G+'" B="'+B+'"/><Viewport.BkFoot.Color R="'+R+'" G="'+G+'" B="'+B+'"/></CLitPropertySet>'
myObject.SetViewport(background_color) 
myObject.RefreshScene(1);
}

function Ground()
{
var is_ground=myObject.GroundGrid
  if(is_ground==false)
  {
  myObject.GroundGrid=1
  }
  else
  {
  myObject.GroundGrid=0
  }

}

function Shadow()
{
var is_shadow=myObject.RenderGroundShadow
  if(is_shadow==false)
  {
  myObject.RenderGroundShadow=1;
  }
  else
  {
  myObject.RenderGroundShadow=0;
  }

}
