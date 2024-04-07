let product_attr_groups = document.querySelectorAll('.product-attr-group')


product_attr_groups.forEach(function (el) {
    let select_inp = el.querySelector('select')
    let option = select_inp.options[select_inp.selectedIndex]
    let additional_price = option.getAttribute('additional-price') || 0
    _set_additional_price(additional_price)
    select_inp.setAttribute('seted-price', additional_price)

    select_inp.addEventListener('change', function () {
        let group_price = Number(select_inp.getAttribute('seted-price')) || 0
        _set_additional_price(-group_price)

        let option = select_inp.options[select_inp.selectedIndex]
        let additional_price = Number(option.getAttribute('additional-price'))
        select_inp.setAttribute('seted-price', additional_price)
        _set_additional_price(additional_price)
    })
})

function _get_original_price_element() {
    return Number(PRICE_ELEMENT.getAttribute('data-price')) || 0
}

function _set_additional_price(price) {
    let price_org = _get_original_price_element()
    price_org += Number(price)
    PRICE_ELEMENT.innerHTML = numberWithCommas(price_org) + ' تومان '
    PRICE_ELEMENT.setAttribute('data-price', price_org)
}

