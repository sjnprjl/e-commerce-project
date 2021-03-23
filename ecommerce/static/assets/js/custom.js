/*==================================================================================
    Custom JS (Any custom js code you want to apply should be defined here).
====================================================================================*/
(function ($) {
    "use strict";
    // filter in js

    const $filterName = $("#filterName");
    const $filterPhone = $("#filterPhone");
    const $entries = $("[data-type='search-item']");
    const $filters = $("[data-type='search-field']");

    $filters.on('keyup', function () {
        const $val = $(this).val().toUpperCase();
        $.each($entries, function () {
            const $name = $(this).children("td")[1];
            const $phone = $(this).children("td")[2];
            const $nameValue = $name.textContent.trim();
            const $phoneValue = $phone.textContent.trim();
            if ($nameValue
                .toUpperCase()
                .indexOf($filterName.val().trim().toUpperCase()) == -1 ||
                $phoneValue.indexOf($filterPhone.val().trim().toUpperCase()) == -1) {
                $(this).addClass('display-none');
            } else {
                $(this).removeClass('display-none');

            }

        })
    });
})(jQuery)



