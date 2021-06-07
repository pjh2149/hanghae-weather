function weather() {
    let cityName = $('#citySelect option:selected').val();
    let cityInput = cityName.replace("''", "");
    $.ajax({
        type: "GET",
        url: `https://api.openweathermap.org/data/2.5/weather?q=${cityInput}&appid=3d9290fe0f2425345dc583eb4d290e52&units=metric`,
        data: {},
        success: function (response) {
            let city = response.name;
            let temp = response.main.temp;
            let description = response.weather[0].description;
            let humidity = response.main.humidity;
            let image = response.weather[0].icon;
            let icon = `<img class="weatherIcon" src="http://openweathermap.org/img/wn/${image}@2x.png">`;
            $('#city').text(city);
            $('#temperature').text(temp + "°");
            $('#description').text(description);
            $('#humidity').text(humidity + "%");
            $('#icon').html(icon);
            console.log(response);
        }
    })
}
