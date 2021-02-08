var in_work=0


function Detail_container_on()
{
  if(in_work==0)
  {
	setBackgroundImage(myObject,"3D");
	
    document.getElementById("3D").onmouseover = function () { Detail_container_off() }
    myObject2.onmouseover = function () { }

  }
}

function Detail_container_off()
{
  if(in_work==0)
  {
  document.getElementById("3D").style.background=""
  myObject.style.visibility = "visible";
  document.getElementById("3D").onmouseover = function () { }
  myObject2.onmouseover = function () { Detail_container_on() }

  }
}
