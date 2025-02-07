# 🧠 BrainFish Project Documentation

## 📚 Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## 🌟 Overview

BrainFish is a modern web application that combines a FastAPI backend with a Vue.js and Svelte frontend. It utilizes Redis for data management and Docker for deployment.

## 🏗️ Project Structure
GET /risk - папка со всеми ассетами, там будут хэши плохих доменов и тд
/risks/blocked-domains.json - хэши заблокированных доменов

["hash1","hash2", ...]

/risks/update.json?revision=... - быстро обновить хэши доменов без полной прогрузки старых

{
"whitelisted": ["hash1","hash2", ...],
"blocked": ["hash1","hash2", ...],
"blocked-assets": ["hash1","hash2", ...],
"phishing-signs": ["*CONNECT WALLET**", "scan qr code", ...]
}

/risks/current-revision

150

/risks/whitelisted-domains.json

["hash1","hash2", ...]

/risks/blocked-assets.json

["hash1","hash2", ...]

/risks/phishing-signs.json

["*CONNECT WALLET**", "scan qr code", ...]


GET / - папка с красивым сайтиком, должно просто статично передаваться


API:
POST /api/report

{
"url":"https://some.com",
"history":["https://google.com/?search=some.com","https://some.com"],
"comment":"пон",
"contents":{"https://some.com/scam.js":"var scam=true,...."},
"pow": {"nonce": 150, "difficulty": 150, "hash": "somehash"}
}

->
204 NO CONTENT

API:
POST /api/allow

{
"url":"https://some.com",
"history":["https://google.com/?search=some.com","https://some.com"],
"comment":"пон",
"contents":{"https://some.com/scam.js":"var scam=true,...."},
"pow": {"nonce": 150, "difficulty": 150, "hash": "somehash"}
}

->
204 No content


POST /api/check

{
"url":"https://some.com",
"history":["https://google.com/?search=some.com","https://some.com"],
"contents":{"https://some.com/scam.js":"var scam=true,...."},
"pow": {"nonce": 150, "difficulty": 150, "hash": "somehash"},
"settings": {"ai": true, "community": true, "advanced": false}
}

->
200 OK

{
"risk": 30,
"reason": {"content": "phishing", "source":"community", "message": "домен был заблокан"}
}


Ошибки:
-> 401 Unauthorised

{
"message": "..."
}

чаще всего когда pow (proof of work) токен неправильный

-> 403 Forbidden 

{
"message": "Вы заблокированы."
}


-> 500 Internal server error

{
"message": "пацаны я прод положил"
}

либо прод упал либо иишка сдохла короче пон

-> 429 Too many requests

{
"message": "ддос"
}


-> 400 Bad Request

{
"message": "ты лох"
}
