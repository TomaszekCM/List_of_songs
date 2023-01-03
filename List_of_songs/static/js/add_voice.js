//$(document).ready(function(){
//
//$("#add").click(function (e){
//event.preventDefault()
//$('#items').append('<div><br><input type="text" name="dodatkowy">' + '<input type = "button" value="delete" id="delete" /></div>');
//
//});
//
//$('body').on('click', '#delete', function (e){
//    $(this).parent('div').remove();
//
//});
//
//
//});

//function myFunction() {
//  alert("I am an alert huge  box!");
//}

function createNewElement() {
    // First create a DIV element.
	var txtNewInputBox = document.createElement('div');

    // Then add the content (a new input box) of the element.
	txtNewInputBox.innerHTML = "<br><input type='text' id='newInputBox' name='newVoice'>";

    // Finally put it where it is supposed to appear.
	document.getElementById("newElementId").appendChild(txtNewInputBox);
}


function createNewElement2(all_tags) {
    var txtNewInputBox2 = document.createElement('div');
    var selectInputBox = document.createElement('select')

    // Then add the content (a new input box) of the element.
	selectInputBox.innerHTML = "<option value=''></option>"
	for (i in all_tags) {

	selectInputBox.innerHTML += "<option value='" + all_tags[i] + "'>" + all_tags[i] + "</option>"
	}

    selectInputBox.setAttribute('name', 'tag');

//    txtNewInputBox2.innerHTML = " &ensp; &ensp; &ensp; &ensp;"
    txtNewInputBox2.appendChild(selectInputBox)
    txtNewInputBox2.innerHTML += "<br><br>"

    // Finally put it where it is supposed to appear.
	document.getElementById("newElementId2").appendChild(txtNewInputBox2);

}


function createNewElement3() {
    // First create a DIV element.
	var txtNewInputBox = document.createElement('div');

    // Then add the content (a new input box) of the element.
	txtNewInputBox.innerHTML = "<br><input type='text' name='tag'>";

    // Finally put it where it is supposed to appear.
	document.getElementById("newElementId3").appendChild(txtNewInputBox);
}