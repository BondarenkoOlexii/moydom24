$(document).ready(function() {

    // 1. Ініціалізуємо звичайний Select2 для країни
    $('#flatform-house_id').select2({
        placeholder: "Выберите дом",
        ajax: {
            url: '/api/house/',
            dataType: 'json',
            delay: 250,
            data: function (params){
                return {
                    q: params.term
                };

            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
            cache: true
        }
    });
//
//    // 2. Ініціалізуємо Select2 для міста з підтримкою AJAX
    $('#flatform-section_id').select2({
        placeholder: "Выберите дом",
        ajax: {
            url: '/api/section/', // URL нашого Django Ninja ендпоінту
            dataType: 'json',
            delay: 250, // Затримка, щоб не спамити запитами при швидкому друку
            data: function (params) {
                return {
                    // Динамічно беремо ID вибраного дому
                    house_id: $('#flatform-house_id').val(),
                    // Відправляємо те, що юзер друкує в полі пошуку Select2
                    q: params.term
                };
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
            cache: true
        }
    });

    $('#flatform-floor_id').select2({
        placeholder: "Выберите дом",
        ajax: {
            url: '/api/storey/', // URL нашого Django Ninja ендпоінту
            dataType: 'json',
            delay: 250, // Затримка, щоб не спамити запитами при швидкому друку
            data: function (params) {
                return {
                    // Динамічно беремо ID вибраної країни
                    house_id: $('#flatform-house_id').val(),
                    // Відправляємо те, що юзер друкує в полі пошуку Select2
                    q: params.term
                };
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
            cache: true
        }
    });

    $('#flatform-apartment_id').select2({

        placeholder: 'Выберите квартиру',
        ajax: {
            url: '/api/apartment/',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    house_id: $('#flatform-house_id').val(),
                    section_id: $('#flatform-section_id').val(),
                    storey_id: $('#flatform-floor_id').val(),
                    q: params.term
                };
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
            cache: true
        }
    });


    $('#invoice-tariff_id').select2({
        placeholder: 'Выберите тариф',
        ajax: {
            url: '/api/tariff/',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    q: params.term
                };
            },

            processResults: function (data) {
                return {
                    results: data
                };
            },
            cache: true
        }
    });



    $('#flatform-apartment_id').on('change', function(){
        var apartmentId = $(this).val();
        var $paymentInput = $('#account_uid');
        var $fullnameSpan = $('#user-fullname');
        var $phonenumSpan = $('#user-phone');

        $paymentInput.val('')

        if (apartmentId) {
            $.ajax({
                url: '/api/payment_account/',
                type: 'GET',
                data: {
                    apartment_id: apartmentId
                },

                success: function(response){
                    if (response && response.length > 0) {
                        $paymentInput.val(response[0].text);
                        $fullnameSpan.text(response[0].full_name);
                        $phonenumSpan.text(response[0].phone_number)

                    } else {
                        $paymentInput.val('Счет не найден')
                    }
                },

            })

        }

    });

    $('#accounttransaction-payment_account').select2({
         ajax: {
            url: '/api/bank_book_ids/',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                        owner_id: $('#w1').val()
                    };
            },

            processResults: function (data) {
                return {
                    results: data
                };
            },
            cache: true
        }
    });


    $('#flatform-apartment_id').on('change', function(){
        var apartmentId = $(this).val();
        var $paymentInput = $('#account-uid');
        var $fullnameSpan = $('#user-fullname');
        var $phonenumSpan = $('#user-phone');

        $paymentInput.val('')

        if (apartmentId) {
            $.ajax({
                url: '/api/bank_book/',
                type: 'GET',
                data: {
                    apartment_id: apartmentId
                },

                success: function(response){
                    if (response && response.length > 0) {
                        $fullnameSpan.text(response[0].full_name);
                        $phonenumSpan.text(response[0].phone_number)

                    } else {
                        $paymentInput.val('Счет не найден')
                    }
                },

            })

        }

    });

    $('#accounttransaction-transaction_purpose_id').select2({
        placeholder: 'Выберите статью',
        ajax: {
            url: '/api/article/',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    q: params.term
                };
            },

            processResults: function (data) {
                return {
                    results: data
                };
            },
            cache: true
        }
    });







    // 3. Логіка блокування/розблокування та очищення
    $('#flatform-house_id').on('change', function() {
        var house_id = $(this).val();
        var $sectionSelect = $('#flatform-section_id');
        var $storeySelect = $('#flatform-floor_id');
        var $apartmentSelect = $('#flatform-apartment_id');

        // Очищаємо попередньо вибране місто
        $sectionSelect.empty().trigger("change");
        $storeySelect.empty().trigger("change");
        $apartmentSelect.empty().trigger("change");


        if (house_id) {
            $sectionSelect.prop('disabled', false);
            $storeySelect.prop('disabled', false);

            if ($sectionSelect) {
                $apartmentSelect.prop('disabled', false);
            }

        } else {
            // Якщо країну скинуто - блокуємо поле міста
            $sectionSelect.prop('disabled', true);
            $storeySelect.prop('disabled', true);
            $apartmentSelect.prop('disabled', true);

            // Додаємо дефолтний option назад
            $sectionSelect.append(new Option("Сначала выберите дом", "", true, true));
            $storeySelect.append(new Option("Сначала выберите дом", "", true, true));
            $apartmentSelect.append(new Option("Сначала выберите...", "", true, true));
        }

        if (!$('#flatform-house_id').val()) {
            $('#flatform-section_id').prop('disabled', true);
            $('#flatform-floor_id').prop('disabled', true);
            $('#flatform-apartment_id').prop('disabled', true);
        }

    });

    $('#w1').on('change', function() {
        var owner_id = $(this).val();
        var $paymentaccountSelect = $('#accounttransaction-payment_account');

        $paymentaccountSelect.empty().trigger("change");

        if (owner_id) {
            $paymentaccountSelect.prop('disabled', false);
        } else {
            $paymentaccountSelect.append(new Option("Сначала выберите пользователя", "", true, true));
        }

    });
});
