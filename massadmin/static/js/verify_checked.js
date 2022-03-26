function verify_checked() {
    checkboxes = document.querySelectorAll("input.update_checkbox");
    some_checked = false;
    for (var i = 0, len = checkboxes.length; i < len; i++) {
        if ( checkboxes[i].checked ) {
        some_checked = true;
        }
    }
    if ( ! some_checked ) {
        some_checked = confirm('You have not checked off any fields to update. Are you sure you wish to continue?');
    }
    return some_checked;
}
