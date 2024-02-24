// -------------------------- Toggle passwords input to text and reverse -------------------------
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


// ---------------------------- Add data to delete address modal -------------------------- //
$('#deleteAddressModal').on('show.bs.modal', function (event) {
    let button = $(event.relatedTarget);
    let pk = button.data('pk');

    let modal = $(this);
    modal.find('.modal-body input[name=pk]').val(pk);
})


// Active tab based on GET parameter
function activeTab() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const tabName = urlParams.get('tab');

    if (tabName === 'address') {
        let tab = document.getElementById('address');
        let tabLink = document.querySelector("a[href='#address']");

        tab.classList.add('active');
        tabLink.classList.add('active');

    } else if (tabName === 'notification') {
        let tab = document.getElementById('notification');
        let tabLink = document.querySelector("a[href='#notification']");

        tab.classList.add('active');
        tabLink.classList.add('active');

    } else if (tabName === 'settings') {
        let tab = document.getElementById('settings');
        let tabLink = document.querySelector("a[href='#settings']");

        tab.classList.add('active');
        tabLink.classList.add('active');

    } else {
        let tab = document.getElementById('personal');
        let tabLink = document.querySelector("a[href='#personal']");

        tab.classList.add('active');
        tabLink.classList.add('active');
    }
}
activeTab();
