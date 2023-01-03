//Functions needed to copy  list of songs

function clearPastSelect() {
    document.getElementById("previous").options[0].selected = 'selected';
}

function clearFutureSelect() {
    document.getElementById("future").options[0].selected = 'selected';
}


//Functions needed for creating list manually

function convertToSeconds(duration) {
    if (duration != "None") {
        let secs_to_add = parseInt(duration.slice(-2));

        let mins_to_add = parseInt(duration.substr(-5, 2));
        secs_to_add += (mins_to_add * 60);

        let hours_to_add = parseInt(duration.substr(-8, 2));
        secs_to_add += (hours_to_add * 60 * 60)

        return secs_to_add
    }
}

function secondsToString(total_time){
    let hours = (total_time / (60*60))  >> 0;
    let minutes = total_time % (60*60);
    clear_minutes = (minutes / 60) >>0;
    let seconds = minutes % 60;

    if (clear_minutes <10) {
        clear_minutes = "0" + clear_minutes;
    }

    if (seconds <10) {
        seconds = "0" + seconds;
    }

    total_time_string = hours + ":" + clear_minutes + ":" + seconds;

    return total_time_string;
}


// obliczyć w pythonie najpierw total time!! i potem po kliknięciu czegokolwiek zczytać zawartość,
// przeliczyć na sekundy itp, po czym działać już wg funkcji.
var time_counter = document.getElementById("time_counter")
//total time in seconds
let total_time = convertToSeconds(time_counter.innerHTML);
let numb_songs_without_times = 0



function addToList(song_id, duration){
    var class_to_search = "selectedSongs " + song_id;
    document.getElementById(class_to_search).style.display = "";

    var checkBox_to_search = "checkbox " + song_id;
    document.getElementById(checkBox_to_search).checked = true;

    //  before counting times we have to define these variables,
    //  and then, after counting, we have to change class
    var song_to_mark_checked = "SongList " + song_id;
    var song_on_the_list = document.getElementById(song_to_mark_checked);

    // now, if song is not already included
    if (!song_on_the_list.classList.contains("selected")){
        if (duration != "None") {
            secs_to_add = convertToSeconds(duration);
            total_time += secs_to_add;
            total_time += 20;

            time_to_display = secondsToString(total_time);
            time_counter.innerHTML = time_to_display;

        } else {
            numb_songs_without_times += 1;
        }
    }

    if (numb_songs_without_times > 0) {
        document.getElementById('not_all_have_times').innerHTML = "<br>Nie wszystkie utwory mają podany czas!";
    }

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

    if (duration != "None") {
            secs_to_add = convertToSeconds(duration);
            total_time -= secs_to_add;
            total_time -= 20;

            time_to_display = secondsToString(total_time);

            time_counter.innerHTML = time_to_display;

        } else {
            numb_songs_without_times -= 1;
        }

    if (numb_songs_without_times == 0) {
        document.getElementById('not_all_have_times').innerHTML = "";
    }

    song_on_the_list.classList.remove("selected");
}