// JavaScript Document



var get_property = new Class({ 
	initialize: function(part_GUID,property_name) {
		this.part_GUID  = part_GUID;
    this.property_name  = property_name; 
	},

	get_property_value: function() { 
		var prop=myObject.GetPropertyValue(this.part_GUID,this.property_name)
      if(prop.indexOf("<CLitPropertySet/>")!=(-1))
      {prop=""}
      else
      {
      var equal_pos=prop.indexOf("=");
      var sign_pos=prop.indexOf("/>");
      prop=prop.substring(equal_pos+2,sign_pos-1); 	
		  }
      return prop;
	}
	
	
	
});





