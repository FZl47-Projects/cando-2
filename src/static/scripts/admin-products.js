function activeField(id, state='false') {
    const inputSection = document.getElementById(id);
    const innerInputs = inputSection.querySelectorAll('input');

    if (state === true) {
        inputSection.classList.remove('d-none');
        innerInputs.forEach((item, index) => {
            item.setAttribute('required', 'required');
        })
    } else {
        inputSection.classList.add('d-none');
        innerInputs.forEach((item, index) => {
            item.removeAttribute('required');
        })
    }
}