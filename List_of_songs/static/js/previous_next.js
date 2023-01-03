document.onkeydown = checkKey;

function checkKey(e) {

    e = e || window.event;

    if (e.keyCode == '39') {
        // up arrow
//        alert("prawy")
        let next_button = document.getElementById('next')
        next_button.click()
    }
        if (e.keyCode == '37') {
        // up arrow
//        alert("lewy")
        let previous_button = document.getElementById('previous')
        previous_button.click()
    }

    }