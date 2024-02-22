// Validation before submit
document.getElementById('addUserForm').addEventListener('submit', (e) => {
    e.preventDefault();
    let password1 = e.target.querySelector('input[name=password]').value;
    let password2 = e.target.querySelector('input[name=password2]').value;

    if (password1 != password2) {
        createNotify({
            title: 'خطا',
            message: 'رمز عبور و تکرار آن یکسان نیست!',
            theme: 'warning'
        })
    } else {
        e.target.submit();
    }
})

// Toggle passwords input to text and reverse
const passToggles = document.querySelectorAll('.pass-toggle');
passToggles.forEach((item, index) => {
    let icon = item.querySelector('.icon');
    let input = item.querySelector('input[type=password]');

    icon.addEventListener('click', function (e) {
        if (input.type === 'password') {
            input.type = 'text';
            icon.classList.replace('ni-eye', 'ni-eye-off');
        } else {
            input.type = 'password';
            icon.classList.replace('ni-eye-off', 'ni-eye');
        }
    })
})


// ---------------------------- Add data to delete user modal -------------------------- //
$('#delete-user').on('show.bs.modal', function (event) {
    let button = $(event.relatedTarget);
    let title = button.data('title');
    let phone = button.data('phone');
    let id = button.data('id');

    let modal = $(this);
    modal.find('.modal-body input[name=id]').val(id);
    modal.find('.modal-body #user-name-title').text(title);
    modal.find('.modal-body #user-phone-title').text(phone);
})
// ------------------------- Add data to delete user modal -------------------------- //
