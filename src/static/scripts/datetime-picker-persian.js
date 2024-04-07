// datetime picker persian
let datetime_pickers = document.querySelectorAll('.datetime-picker')
for (let picker of datetime_pickers) {
    let picker_inp = picker
    $(picker).mpdatepicker({
        autoClose: true,
        timePicker: false,
    });
}