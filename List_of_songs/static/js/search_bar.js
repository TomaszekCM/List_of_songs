function myFunction() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    ul = document.getElementById("myOL");
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}


var used_tags = []


function setSearchTags() {
    var current_tag = document.getElementById("mySelect");
    current_tag = current_tag.value;
    var selected_tags = document.getElementById("selected_tags");
    var selected_tag = document.getElementById(current_tag);
    selected_tag.classList.remove("hidden");

    var already_includes = false
    for (var i = 0; i < used_tags.length; i++) {
        if (used_tags[i] == current_tag){
            already_includes = true;
            }
    }
    if (!already_includes) {
      used_tags.push(current_tag);
    }

    showSongsWithTags(used_tags);
}


function removeFilter(tag) {

    var tagToHide = document.getElementById(tag);
    tagToHide.classList.add("hidden");

    for (var i = 0; i < used_tags.length; i++){
        if (used_tags[i] == tag) {
            used_tags.splice(i, 1);
            break;
        }
    }

    showSongsWithTags(used_tags);
}


function showSongsWithTags(all_used_tags) {

  let lst = document.getElementsByClassName("song");
  for (piosenka_idx = 0; piosenka_idx < lst.length; piosenka_idx++) {

    var visible = true;
    for (tag_idx = 0; tag_idx < all_used_tags.length; tag_idx++) {
      if (!lst[piosenka_idx].classList.contains(all_used_tags[tag_idx])) {
        visible = false;
      }
    }
    if (visible) {
      lst[piosenka_idx].classList.remove("hidden");
    } else {
      lst[piosenka_idx].classList.add("hidden");
    }
  }
}

//SEARCH USING DIV ELEMENT - for views without lists
//function myFunction() {
//    var input, filter, ul, li, a, i, txtValue;
//    input = document.getElementById("myInput");
//    filter = input.value.toUpperCase();
//    div = document.getElementById("myDiv");
////    div = ul.getElementsByTagName("div");
//    for (i = 0; i < div.length; i++) {
//        a = div[i].getElementsByTagName("a")[0];
////        a = li.getElementsByTagName("a");
//        txtValue = a.textContent || a.innerText;
//        if (txtValue.toUpperCase().indexOf(filter) > -1) {
//            div[i].style.display = "";
//        } else {
//            div[i].style.display = "none";
//        }
//    }
//}