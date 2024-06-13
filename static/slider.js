document.addEventListener('DOMContentLoaded', function () {
    var slider = document.getElementById('slider');
    var sliderValue = document.getElementById('slider-value');
    var form = document.getElementById('recomendacionesForm');
    var sliderInput = document.getElementById('sliderInput');

    noUiSlider.create(slider, {
        start: [parseInt(sliderInput.value)],
        step: 1,
        range: {
            'min': 1,
            'max': 10
        },
        tooltips: true,
        format: {
            to: function (value) {
                return value.toFixed(0);
            },
            from: function (value) {
                return Number(value);
            }
        }
    });

    slider.noUiSlider.on('update', function (values, handle) {
        var value = values[handle];
        sliderValue.innerHTML = value;
        sliderInput.value = value;
    });

    slider.noUiSlider.on('change', function () {
        form.submit();
    });
});