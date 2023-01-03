//Functions needed to copy  list of songs

function clearPastSelect() {
    document.getElementById("previous").options[0].selected = 'selected';
}

function clearFutureSelect() {
    document.getElementById("future").options[0].selected = 'selected';
}


//Functions needed for creating list manually

function addToList(song_id, duration){
    var class_to_search = "selectedSongs " + song_id;
    document.getElementById(class_to_search).style.display = "";

    var checkBox_to_search = "checkbox " + song_id;
    document.getElementById(checkBox_to_search).checked = true;

    //  before counting times we have to define these variables,
    //  and then, after counting, we have to change class
    var song_to_mark_checked = "SongList " + song_id;
    var song_on_the_list = document.getElementById(song_to_mark_checked);

//    finally, we have to make selected song green on the list
    song_on_the_list.classList.add("selected");
}


function removeFromList(song_id, duration){
    var class_to_search = "selectedSongs " + song_id;
    document.getElementById(class_to_search).style.display = "none";

    var checkBox_to_search = "checkbox " + song_id;
    document.getElementById(checkBox_to_search).checked = false;

    var song_to_mark_checked = "SongList " + song_id;
    var song_on_the_list = document.getElementById(song_to_mark_checked);

    song_on_the_list.classList.remove("selected");
}