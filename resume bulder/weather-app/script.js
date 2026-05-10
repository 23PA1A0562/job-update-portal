const searchBtn = document.getElementById('search-btn');
const locationBtn = document.getElementById('location-btn');
const cityInput = document.getElementById('city-input');
const weatherInfo = document.getElementById('weather-info');
const errorMessage = document.getElementById('error-message');

const temperatureEl = document.getElementById('temperature');
const cityNameEl = document.getElementById('city-name');
const weatherConditionEl = document.getElementById('weather-condition');
const humidityEl = document.getElementById('humidity');
const windSpeedEl = document.getElementById('wind-speed');
const weatherIconEl = document.getElementById('weather-icon');

// New DOM Elements for advanced statistics
const aqiEl = document.getElementById('aqi');
const uvIndexEl = document.getElementById('uv-index');
const pressureEl = document.getElementById('pressure');

// Toggle Elements
const unitToggle = document.getElementById('unit-toggle');
const celsiusBtn = document.getElementById('celsius-btn');
const fahrenheitBtn = document.getElementById('fahrenheit-btn');

// Tab Elements
const tabWeather = document.getElementById('tab-weather');
const tabDrive = document.getElementById('tab-drive');
const weatherSearchBox = document.getElementById('weather-search-box');
const driveSearchBox = document.getElementById('drive-search-box');
const driveResults = document.getElementById('drive-results');

// Drive Planner Elements
const originInput = document.getElementById('origin-input');
const destInput = document.getElementById('dest-input');
const planDriveBtn = document.getElementById('plan-drive-btn');
const driveDistance = document.getElementById('drive-distance');
const driveDuration = document.getElementById('drive-duration');
const driveSafetyCard = document.getElementById('drive-safety-card');
const driveStatus = document.getElementById('drive-status');
const driveReason = document.getElementById('drive-reason');

let currentUnit = 'metric'; // 'metric' for Celsius, 'imperial' for Fahrenheit
let currentTempC = null; // store current temp in Celsius

// Day / Night Themes!
const backgrounds = {
    'Clear': {
        day: 'url("https://images.unsplash.com/photo-1601297183305-6df142704ea2?q=80&w=2560&auto=format&fit=crop")',
        night: 'url("https://images.unsplash.com/photo-1507400492013-162706c8c05e?q=80&w=2560&auto=format&fit=crop")'
    },
    'Clouds': {
        day: 'url("https://images.unsplash.com/photo-1534088568595-a066f410cbda?q=80&w=2560&auto=format&fit=crop")',
        night: 'url("https://images.unsplash.com/photo-1534274988757-a28bf1a57c17?q=80&w=2560&auto=format&fit=crop")'
    },
    'Rain': {
        day: 'url("https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?q=80&w=2560&auto=format&fit=crop")',
        night: 'url("https://images.unsplash.com/photo-1428592953211-077101b2021b?q=80&w=2560&auto=format&fit=crop")'
    },
    'Thunderstorm': {
        day: 'url("https://images.unsplash.com/photo-1605727216801-e27ce1d0ce3c?q=80&w=2560&auto=format&fit=crop")',
        night: 'url("https://images.unsplash.com/photo-1605727216801-e27ce1d0ce3c?q=80&w=2560&auto=format&fit=crop")'
    },
    'Snow': {
        day: 'url("https://images.unsplash.com/photo-1491002052546-bf38f186af56?q=80&w=2560&auto=format&fit=crop")',
        night: 'url("https://images.unsplash.com/photo-1542601098-8fc114e148e2?q=80&w=2560&auto=format&fit=crop")'
    },
    'Mist': {
        day: 'url("https://images.unsplash.com/photo-1543968996-ee822b817625?q=80&w=2560&auto=format&fit=crop")',
        night: 'url("https://images.unsplash.com/photo-1543968996-ee822b817625?q=80&w=2560&auto=format&fit=crop")'
    },
    'Default': {
        day: 'url("https://images.unsplash.com/photo-1534088568595-a066f410cbda?q=80&w=2560&auto=format&fit=crop")',
        night: 'url("https://images.unsplash.com/photo-1507400492013-162706c8c05e?q=80&w=2560&auto=format&fit=crop")'
    }
};

// Free Open-Meteo API mapping
const wmoToCondition = {
    0: { main: 'Clear', icon: '01d' },
    1: { main: 'Clear', icon: '02d' },
    2: { main: 'Clouds', icon: '03d' },
    3: { main: 'Clouds', icon: '04d' },
    45: { main: 'Mist', icon: '50d' },
    48: { main: 'Mist', icon: '50d' },
    51: { main: 'Rain', icon: '09d' },
    53: { main: 'Rain', icon: '09d' },
    55: { main: 'Rain', icon: '09d' },
    56: { main: 'Rain', icon: '09d' },
    57: { main: 'Rain', icon: '09d' },
    61: { main: 'Rain', icon: '10d' },
    63: { main: 'Rain', icon: '10d' },
    65: { main: 'Rain', icon: '10d' },
    66: { main: 'Rain', icon: '10d' },
    67: { main: 'Rain', icon: '10d' },
    71: { main: 'Snow', icon: '13d' },
    73: { main: 'Snow', icon: '13d' },
    75: { main: 'Snow', icon: '13d' },
    77: { main: 'Snow', icon: '13d' },
    80: { main: 'Rain', icon: '09d' },
    81: { main: 'Rain', icon: '09d' },
    82: { main: 'Rain', icon: '09d' },
    85: { main: 'Snow', icon: '13d' },
    86: { main: 'Snow', icon: '13d' },
    95: { main: 'Thunderstorm', icon: '11d' },
    96: { main: 'Thunderstorm', icon: '11d' },
    99: { main: 'Thunderstorm', icon: '11d' }
};

// Tabs Logic
tabWeather.addEventListener('click', () => {
    tabWeather.style.background = 'rgba(255,255,255,0.2)';
    tabDrive.style.background = 'transparent';
    weatherSearchBox.style.display = 'flex';
    driveSearchBox.style.display = 'none';
    driveResults.style.display = 'none';
    if(cityNameEl.textContent !== '--') weatherInfo.style.display = 'block';
});

tabDrive.addEventListener('click', () => {
    tabDrive.style.background = 'rgba(255,255,255,0.2)';
    tabWeather.style.background = 'transparent';
    weatherSearchBox.style.display = 'none';
    driveSearchBox.style.display = 'flex';
    weatherInfo.style.display = 'none';
});

// Event Listeners
searchBtn.addEventListener('click', () => {
    const city = cityInput.value.trim();
    if (city !== "") getWeatherData(city);
});

cityInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const city = cityInput.value.trim();
        if (city !== "") getWeatherData(city);
    }
});

locationBtn.addEventListener('click', () => {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const { latitude, longitude } = position.coords;
            getWeatherByCoords(latitude, longitude);
        }, () => {
            alert("Unable to retrieve your location.");
        });
    } else {
        alert("Geolocation is not supported by your browser.");
    }
});

planDriveBtn.addEventListener('click', () => {
    const origin = originInput.value.trim();
    const dest = destInput.value.trim();
    if (origin !== "" && dest !== "") {
        planRoute(origin, dest);
    }
});

unitToggle.addEventListener('click', () => {
    if (currentUnit === 'metric') {
        currentUnit = 'imperial';
        celsiusBtn.style.background = 'transparent';
        celsiusBtn.style.color = '#fff';
        fahrenheitBtn.style.background = '#fff';
        fahrenheitBtn.style.color = '#1e3c72';
    } else {
        currentUnit = 'metric';
        fahrenheitBtn.style.background = 'transparent';
        fahrenheitBtn.style.color = '#fff';
        celsiusBtn.style.background = '#fff';
        celsiusBtn.style.color = '#1e3c72';
    }
    updateTemperatureDisplay();
});

// Initial auto-detect
window.addEventListener('DOMContentLoaded', () => {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const { latitude, longitude } = position.coords;
            getWeatherByCoords(latitude, longitude);
        });
    }
});

async function getGeoCoords(city) {
    const geoUrl = `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(city)}&count=1&language=en&format=json`;
    const geoResponse = await fetch(geoUrl);
    const geoData = await geoResponse.json();
    if (!geoData.results || geoData.results.length === 0) throw new Error("City not found: " + city);
    return geoData.results[0];
}

async function getWeatherData(city) {
    try {
        errorMessage.style.display = 'none';
        weatherInfo.classList.remove('active');
        const coords = await getGeoCoords(city);
        await fetchAndDisplayWeather(coords.latitude, coords.longitude, coords.name);
    } catch (error) {
        errorMessage.style.display = 'block';
    }
}

async function getWeatherByCoords(lat, lon) {
    try {
        errorMessage.style.display = 'none';
        weatherInfo.classList.remove('active');
        cityInput.value = '';
        
        let locationName = "Unknown Location";
        try {
            const reverseGeoUrl = `https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${lat}&longitude=${lon}&localityLanguage=en`;
            const reverseGeoResponse = await fetch(reverseGeoUrl);
            const reverseGeoData = await reverseGeoResponse.json();
            locationName = reverseGeoData.city || reverseGeoData.locality || reverseGeoData.principalSubdivision || "Your Area";
        } catch(e) {
            locationName = "Your Area";
        }
        
        await fetchAndDisplayWeather(lat, lon, locationName);
    } catch (error) {
        errorMessage.style.display = 'block';
    }
}

async function fetchAndDisplayWeather(lat, lon, locationName) {
    try {
        const weatherUrl = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,surface_pressure,is_day`;
        const airQualityUrl = `https://air-quality-api.open-meteo.com/v1/air-quality?latitude=${lat}&longitude=${lon}&current=us_aqi,uv_index`;

        const [weatherResponse, aqiResponse] = await Promise.all([
            fetch(weatherUrl),
            fetch(airQualityUrl)
        ]);
        
        if (!weatherResponse.ok) throw new Error("Location not found");
        
        const weatherData = await weatherResponse.json();
        const aqiData = aqiResponse.ok ? await aqiResponse.json() : null;
        
        const current = weatherData.current;
        const currentAqi = aqiData ? aqiData.current : {};
        
        const weatherMapping = wmoToCondition[current.weather_code] || { main: 'Unknown', icon: '03d' };
        
        let iconCode = weatherMapping.icon;
        if (current.is_day === 0) iconCode = iconCode.replace('d', 'n');
        
        updateUI({
            temp: current.temperature_2m,
            name: locationName,
            condition: weatherMapping.main,
            humidity: current.relative_humidity_2m,
            windSpeed: current.wind_speed_10m,
            pressure: current.surface_pressure,
            aqi: currentAqi.us_aqi,
            uv: currentAqi.uv_index,
            iconCode: iconCode,
            isDay: current.is_day
        });
        
        weatherInfo.style.display = 'block';
    } catch (error) {
        errorMessage.style.display = 'block';
    }
}

function updateUI(data) {
    currentTempC = data.temp;
    updateTemperatureDisplay();
    
    cityNameEl.textContent = data.name;
    weatherConditionEl.textContent = data.condition;
    humidityEl.textContent = `${data.humidity}%`;
    windSpeedEl.textContent = `${Math.round(data.windSpeed)} km/h`; 
    
    pressureEl.textContent = data.pressure ? `${Math.round(data.pressure)} hPa` : "N/A";
    aqiEl.textContent = data.aqi !== undefined ? data.aqi : "N/A";
    uvIndexEl.textContent = data.uv !== undefined ? data.uv : "N/A";
    
    weatherIconEl.src = `https://openweathermap.org/img/wn/${data.iconCode}@4x.png`;
    
    const timeOfDay = data.isDay === 1 ? 'day' : 'night';
    const conditionBackgrounds = backgrounds[data.condition] || backgrounds['Default'];
    document.body.style.backgroundImage = conditionBackgrounds[timeOfDay];
    
    weatherInfo.classList.add('active');
}

function updateTemperatureDisplay() {
    if (currentTempC === null) return; 
    if (currentUnit === 'metric') {
        temperatureEl.textContent = `${Math.round(currentTempC)}°C`;
    } else {
        const tempF = (currentTempC * 9/5) + 32;
        temperatureEl.textContent = `${Math.round(tempF)}°F`;
    }
}

// Drive Planner Logic
async function planRoute(origin, dest) {
    try {
        errorMessage.style.display = 'none';
        driveResults.style.display = 'none';
        
        // 1. Geocode both locations
        const origCoords = await getGeoCoords(origin);
        const destCoords = await getGeoCoords(dest);
        
        // 2. Fetch Route from OSRM
        const osrmUrl = `https://router.project-osrm.org/route/v1/driving/${origCoords.longitude},${origCoords.latitude};${destCoords.longitude},${destCoords.latitude}?overview=false`;
        const routeRes = await fetch(osrmUrl);
        const routeData = await routeRes.json();
        
        if(routeData.code !== 'Ok') throw new Error("Could not find a driving route.");
        
        const durationSec = routeData.routes[0].duration;
        const distanceKm = routeData.routes[0].distance / 1000;
        
        // 3. Fetch Destination Weather
        const weatherUrl = `https://api.open-meteo.com/v1/forecast?latitude=${destCoords.latitude}&longitude=${destCoords.longitude}&current=weather_code`;
        const weatherRes = await fetch(weatherUrl);
        const weatherData = await weatherRes.json();
        const condition = wmoToCondition[weatherData.current.weather_code].main;
        
        // Update UI
        driveDistance.textContent = `Distance: ${Math.round(distanceKm)} km`;
        driveDuration.textContent = `Est. Drive Time: ${Math.round(durationSec / 3600)} hours ${Math.round((durationSec % 3600) / 60)} mins`;
        
        if (['Rain', 'Snow', 'Thunderstorm', 'Mist'].includes(condition)) {
            driveSafetyCard.style.background = '#e74c3c'; // Red
            driveStatus.textContent = 'Caution Advised!';
            driveReason.textContent = `Heavy ${condition.toLowerCase()} expected at destination. Drive safely.`;
        } else {
            driveSafetyCard.style.background = '#2ecc71'; // Green
            driveStatus.textContent = 'Safe to Drive!';
            driveReason.textContent = `Clear skies and good conditions expected.`;
        }
        
        driveResults.style.display = 'block';
    } catch (e) {
        console.error(e);
        errorMessage.style.display = 'block';
        errorMessage.textContent = "Could not calculate route. Please check city names.";
    }
}
