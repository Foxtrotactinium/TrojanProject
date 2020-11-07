// JavaScript Document

var is_view = 0;
var is_bom = 0;
var is_pmi = 0;
var is_meta = 0;
var is_tree = 0;
var is_3d_window = 0;
var is_playerpro = "";
var is_Advanced_Template_Open = "";
var is_Digger_Disabled = 0;

function init_template(topbar, bottombar, topmagnetbar, bomtable, viewtable, pmilist, detail_view, web_tree, meta_block) {

    ///////// checks the Playe rPro licence availibilty //////////////
    is_playerpro = myObject.IsPlayerPro();
    is_Digger_Disabled = myObject.IsDiggerDisabled();

    if (is_playerpro == false) {
        //Below function checks if the file is non-DS file and then convert it to simple template (also displays the license related messages)
        ConvertAdvanceToSimpleTemplate(bottombar, bomtable, viewtable, pmilist, detail_view, web_tree, meta_block);

        //Update the "is_playerpro" as it is used in this function
        is_playerpro = (myObject.GetOptionsPro() & 16) > 0;

        //Below condition is required  to show the magnetbar when we open Non-DS file in BOM Template without licence
        //Make the "topmagnetbar" variable true for making it Simple template
        if (is_playerpro == false)
            topmagnetbar = true;
    }

    //initiate the variables first, before launching the modules
    if (bomtable == true) { is_bom = 1; }
    if (pmilist == true) { is_pmi = 1; }
    if (meta_block == true) { is_meta = 1; }
    if (web_tree == true) { is_tree = 1; }
    if (detail_view == true) { is_3d_window = 1; }
    if (viewtable == true) { is_view = 1; }

    $('#dialogs').load('resources\\modules\\m_prop\\index.html', function () {
        if (is_3d_window == 1) { document.getElementById('detail_view_prop_container').style.display = "block" }
        initDialogs();
    });


    if (topbar == true && is_playerpro == true) {
        // load Top Bar
        $('#top_bar').load('resources\\sys\\topbar.html');
        $('#top_bar').removeClass('top_cell_close');
        $('#top_bar').addClass('top_cell_open');
    }

    if (bottombar == true && is_playerpro == true) {
        // load Bottom Bar
        $('#bottom_loading').fadeIn();
        $('#bottom_bar').load('resources\\sys\\bottombar.html', function () {
            $('#bottom_bar').removeClass('bottom_cell_close');
            $('#bottom_bar').addClass('bottom_cell_open');
            $('#top_table').removeClass('top_tableNormal');
            $('#top_table').addClass('top_table_withBottom');
            loadTemplateAreas(bomtable, viewtable, pmilist, meta_block, detail_view, is_playerpro);
        });
    }

    if (topmagnetbar == true) {
        // load magnet Bar
        $('#magnet_bar').load('resources\\sys\\topmagnetbar.html');
        $('#magnet_bar').removeClass('top_cell_close');
        $('#magnet_bar').addClass('top_magnetcell_open');
        if (is_playerpro == false)
        {
            $('#digger_command').fadeOut();
            $('#showall_command').fadeOut();
        }
        else if (is_Digger_Disabled == 1)
        {
            $('#digger_command').fadeOut();
        }
    }

    if (web_tree == true && is_playerpro == true) {
        //loads the web assembly tree Window
        $('#leftbloc').fadeIn();
        $('#Tree_area').fadeIn();
        $('#Tree_area').load('resources\\modules\\m_tree\\index.html', function () {
            $('#3D_object').removeClass('normal_3D_object');
            $('#3D_object').addClass('objectWithLeftBlock');
            //Below code is added to fix the issue of tree expand on tree/BOM highlight
            $('#3D_object').mouseenter(function () {
                expand_tree = 1;
            });
            $('#3D_object').mouseleave(function () {
                expand_tree = 0;
            });
        });
    }

    /*if (prop_win == true){
    //loads the BOM table
    $('#Prop_area').load('modules\\m_prop\\index.html');
    if(is_pmi==1)
      {document.getElementById('PMI_colors_option').style.display='block';}     
    } */


    $('#bottom_loading').fadeOut();

    //Below function manages the switch between advance and simple template if we open file through button
    ManageTemplateVisibilty();

}

function loadTemplateAreas(bomtable, viewtable, pmilist, meta_block, detail_view, is_playerpro) {
    if (is_playerpro) {
        if (bomtable == true)
            loadBOMArea();
        if (viewtable == true)
            loadViewArea();
        if (pmilist == true)
            loadPMIArea();
        if (detail_view == true)
            loadDetailViewArea();
    }
    if (meta_block == true)
        loadMetaArea();
}

function loadBOMArea() {
    //loads the BOM table
    $('#Bom_area').fadeIn();
    $('#Bom_area').load('resources\\modules\\m_bom\\index.html');
}

function loadViewArea() {
    //loads the View table
    $('#View_area').fadeIn();
    $('#View_area').load('resources\\modules\\m_views\\index.html');
}

function loadPMIArea() {
    //loads the PMI table
    $('#PMI_area').fadeIn();
    $('#PMI_area').load('resources\\modules\\m_pmi\\index.html');
}

function loadMetaArea() {
    //loads the Meta table
    $('#Meta_area').fadeIn();
    $('#Meta_area').load('resources\\modules\\m_meta\\index.html');
}

function loadDetailViewArea() {
    //loads the detail_view Window
    $('#dialog_detail_view').fadeIn();
    $('#dialog_detail_view').load('resources\\modules\\m_3dwindow\\index.html', function () {
        /*****************loads the Object1 model in Object2*******************/
        var modelFileName = myObject.FileName;
        myObject2.FileName = modelFileName;
        /************************************************************************/
    });
    $('#dialog_detail_view').mouseenter(function () {
        Detail_container_on();
    });
}

function initDialogs() {
    $("#dialog_help").dialog({
        bgiframe: true, autoOpen: false, height: 'auto', modal: true, draggable: true, resizable: false,
        close: function () {
            document.getElementById("3D").style.background = ""
            myObject.style.visibility = "visible"
        }
    });

    $("#App_prop").dialog({
        bgiframe: true, autoOpen: false, width: 400, height: 'auto', modal: true, draggable: true, resizable: false,
        close: function () {
            document.getElementById("3D").style.background = ""
            myObject.style.visibility = "visible"
        },
        buttons: {
            'Close': function () {
                $(this).dialog('close');
                document.getElementById("3D").style.background = ""
                myObject.style.display = "block"
            }
        }
    });

    $("#slider1").slider({
        range: "min",
        value: 37,
        min: 0,
        max: 100,
        slide: function (event, ui) {
            $("#amount1").val(ui.value);
        },
        stop: function (event, ui) {
            var value = $("#slider1").slider("option", "value");
            myObject.CameraSmoothTime = value
        }
    });

    $("#slider2").slider({
        range: "min",
        value: 37,
        min: 0,
        max: 100,
        slide: function (event, ui) {
            $("#amount2").val(ui.value);
        },
        stop: function (event, ui) {
            var value = $("#slider2").slider("option", "value");
            myObject2.CameraSmoothTime = value
        }
    });
}

function ConvertAdvanceToSimpleTemplate(bottombar, bomtable, viewtable, pmilist, detail_view, web_tree, meta_block) {

    //Below condition need to check process is start from advanced template
    if (bottombar || bomtable || viewtable || pmilist || detail_view || web_tree || meta_block)
        is_Advanced_Template_Open = true;

    //Check if the template is simple or not:
    if (is_Advanced_Template_Open) {

        //Check if the file is DS Sample:
        var is_DS_Sample_File = (myObject.GetOptionsPro() & 16) > 0;

        //set all the variables as false for making Simple Template:
        if (is_DS_Sample_File == false) {

            bottombar = false;
            bomtable = false;
            viewtable = false;
            pmilist = false;
            detail_view = false;
            web_tree = false;
            meta_block = false;

            //Here we show the magnetbar <div> for customer file (required for simple template)
            document.getElementById('magnet_bar').style.display = 'block';

            //Set the width when we open customer file 
            document.getElementById('3D_object').setAttribute("style", "width:100%");
        }

        //Below code is used for following scenario:
        //1. DS sample file is used with BOM template (magnet bar is OFF)
        //2. Open Customer file (magnet bar will be ON)
        //3. Again open DS sample (need to make magnet bar again OFF)
        if ((web_tree == false) && (bomtable && viewtable))
            document.getElementById('magnet_bar').style.display = 'none';

        //Below code is used for following scenario:
        //1. Customer file is open (Width  = 100%)
        //2. DS sample is open which has web_tree as TRUE (make width=79%)
        if (web_tree == true)
            document.getElementById('3D_object').setAttribute("style", "width:79%");

        //Display licence related messages
        ShowLicenseMessage(is_DS_Sample_File);

    }
}

function ShowLicenseMessage(is_DS_Sample_File) {

    var License_Text_Message = document.getElementById("top_bar");
    License_Text_Message.setAttribute('style', 'font-size: 15px; cursor: pointer;');
    License_Text_Message.style.textAlign = 'center';
    License_Text_Message.value = License_Text_Message.value;
    License_Text_Message.style.color = 'orange';
    License_Text_Message.style.fontStyle = "oblique";

    if (is_DS_Sample_File) {
        //For DS sample file, provide the advance template functionality and give the below message:
        License_Text_Message.innerHTML = "A Player Pro license is usually necessary to use advanced features, and no such license has been detected on your system. However, you are using a Composer built-in sample, which gives you exclusive access to its advanced features";
    }
    else {
        //For non-DS sample files, redirect to simple template and give the below message:
        License_Text_Message.innerHTML = "A Player Pro license is necessary to use advanced features. Since no such license has been detected on your system, you can only access basic features. Consider purchasing a Player Pro license if you want to use advanced features";
    }
}

function HideFullTemplate() {

    //For simple template hide the <div> of Advanced template:
    document.getElementById('bottom_bar').style.display = 'none';
    document.getElementById('Tree_area').style.display = 'none';
    document.getElementById('dialog_detail_view').style.display = 'none';
    document.getElementById('leftbloc').style.display = 'none';

    //Adjust the height when we open customer file:
    if (file_opened_from_button) {
        document.getElementById('top_table').setAttribute("style", "height:80%");
    }

}

function ShowFullTemplate() {

    //This code is written for the case when DS sample file is opened from Customer file. Here we show the <div> of Advanced template:

    //Make the assembly tree <div> visible:
    if (is_tree) {
        document.getElementById('Tree_area').style.display = 'block';
        document.getElementById('leftbloc').style.display = 'block';
    }

    //Adjust the height from Simple to advance when bottom area is ON
    if (is_pmi || is_meta || is_bom || is_view)
        document.getElementById('top_table').setAttribute("style", "height:60%")

    //Make the detail view <div> visible:
    if (is_3d_window)
        document.getElementById('dialog_detail_view').style.display = 'block';

    //Make the bottom bar <div> visible:
    document.getElementById('bottom_bar').style.display = 'block';
}

function ManageTemplateVisibilty() {
    if (myObject.IsPlayerPro())
        return;

    //If the license not found then provide advance template for DS files
    var isDSSampleFile = (myObject.GetOptionsPro() & 16) > 0;

    if (isDSSampleFile) {
        //Below code is used to show all the <div> of Advanced template
        if (file_opened_from_button) {
            ShowFullTemplate();
        }
    }
    else {
        //Below code is used to hide all the <div> of Advanced template
        HideFullTemplate();
    }
}
