<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Agriculture & Irrigation Portal</title>
    <script src="https://jsdelivr.net"></script>
    <style>
        .alert-pulse { animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: .5; } }
    </style>
</head>
<body class="bg-gray-900 text-gray-100 min-h-screen font-sans">

    <!-- Top Navigation Bar -->
    <header class="bg-gray-800 border-b border-gray-700 p-4 sticky top-0 z-50 shadow-md">
        <div class="max-w-7xl mx-auto flex justify-between items-center">
            <h1 class="text-2xl font-bold text-emerald-400 flex items-center gap-2">
                🌱 SmartAgri Portal <span class="text-xs bg-emerald-500/20 text-emerald-300 px-2 py-1 rounded">v1.0-Stable</span>
            </h1>
            <div id="global-alert-banner"></div>
        </div>
    </header>

    <main class="max-w-7xl mx-auto p-4 md:p-6 space-y-6">

        <!-- Analytics Overview & Controls -->
        <section class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <!-- Filter Controls -->
            <div class="bg-gray-800 p-4 rounded-xl border border-gray-700 shadow flex flex-col justify-between">
                <label for="cropFilter" class="block text-sm font-medium text-gray-400 mb-2">Filter by Crop Type</label>
                <select id="cropFilter" onchange="filterFields()" class="w-full bg-gray-700 text-white rounded-lg p-2 border border-gray-600 focus:outline-none focus:border-emerald-500">
                    <option value="all">All Crops</option>
                    <option value="Wheat">Wheat</option>
                    <option value="Corn">Corn</option>
                    <option value="Rice">Rice</option>
                    <option value="Soybean">Soybean</option>
                    <option value="Cotton">Cotton</option>
                </select>
            </div>

            <!-- Total Consumption Metric -->
            <div class="bg-gray-800 p-4 rounded-xl border border-gray-700 shadow">
                <p class="text-sm font-medium text-gray-400">Total Water Consumption</p>
                <p id="totalWater" class="text-3xl font-bold text-blue-400 mt-2">0 L</p>
                <p class="text-xs text-gray-500 mt-1">Target: <span class="text-emerald-400">< 15,000L daily</span></p>
            </div>

            <!-- Lowest Moisture Field Identifier -->
            <div class="bg-gray-800 p-4 rounded-xl border border-gray-700 shadow">
                <p class="text-sm font-medium text-gray-400">Lowest Soil Moisture</p>
                <p id="lowestMoistureField" class="text-3xl font-bold text-red-400 mt-2">N/A</p>
                <p id="lowestMoistureValue" class="text-xs text-gray-500 mt-1">Critical status tracking</p>
            </div>

            <!-- Water Saving Progress -->
            <div class="bg-gray-800 p-4 rounded-xl border border-gray-700 shadow">
                <p class="text-sm font-medium text-gray-400">Water Conservation Status</p>
                <div class="w-full bg-gray-700 rounded-full h-3 mt-4">
                    <div class="bg-emerald-500 h-3 rounded-full" style="width: 82%"></div>
                </div>
                <p class="text-xs text-gray-400 mt-2">82% of conservation targets achieved</p>
            </div>
        </section>

        <!-- Prioritized Recommendation Engine -->
        <section class="bg-gray-800/60 p-4 rounded-xl border border-gray-700">
            <h2 class="text-lg font-semibold text-emerald-400 mb-3 flex items-center gap-2">
                📋 Prioritized Irrigation Recommendation Engine
            </h2>
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="border-b border-gray-700 text-gray-400 text-sm">
                            <th class="p-2">Priority</th>
                            <th class="p-2">Field ID</th>
                            <th class="p-2">Crop Type</th>
                            <th class="p-2">Action Required</th>
                            <th class="p-2">Completion Status</th>
                        </tr>
                    </thead>
                    <tbody id="recommendationTable" class="text-sm">
                        <!-- Dynamic Content -->
                    </tbody>
                </table>
            </div>
        </section>

        <!-- Main Fields Dashboard Grid -->
        <section>
            <h2 class="text-xl font-bold mb-4 text-gray-200">Field Monitoring Dashboards</h2>
            <div id="fieldsGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <!-- Dynamic Field Cards -->
            </div>
        </section>
    </main>

    <script>
        // Simulated Live Sensor Data Matrix
        const agriculturalFields = [
            { id: "FIELD-01", crop: "Wheat", moisture: 24, waterConsumption: 2500, temp: 28, schedule: "Immediate", health: "Stressed" },
            { id: "FIELD-02", crop: "Corn", moisture: 45, waterConsumption: 3100, temp: 31, schedule: "In 6 Hours", health: "Optimal" },
            { id: "FIELD-03", crop: "Rice", moisture: 18, waterConsumption: 4200, temp: 29, schedule: "Immediate", health: "Critical" },
            { id: "FIELD-04", crop: "Soybean", moisture: 55, waterConsumption: 1800, temp: 26, schedule: "In 24 Hours", health: "Optimal" },
            { id: "FIELD-05", crop: "Cotton", moisture: 38, waterConsumption: 2200, temp: 33, schedule: "In 12 Hours", health: "Good" }
        ];

        function initDashboard() {
            renderDashboard(agriculturalFields);
            calculateAnalytics(agriculturalFields);
            generateRecommendations(agriculturalFields);
        }

        function renderDashboard(fields) {
            const grid = document.getElementById("fieldsGrid");
            grid.innerHTML = "";

            fields.forEach(field => {
                const isAlert = field.moisture < 30;
                const card = document.createElement("div");
                card.className = `p-5 rounded-xl border transition-all bg-gray-800 ${isAlert ? 'border-red-500/50 shadow-lg shadow-red-950/20' : 'border-gray-700'}`;
                
                card.innerHTML = `
                    <div class="flex justify-between items-start mb-4">
                        <div>
                            <h3 class="text-lg font-bold text-white">${field.id}</h3>
                            <p class="text-xs text-emerald-400 font-semibold">${field.crop}</p>
                        </div>
                        <span class="px-2 py-1 rounded text-xs font-bold ${isAlert ? 'bg-red-500/20 text-red-400 alert-pulse' : 'bg-gray-700 text-gray-300'}">
                            ${isAlert ? '⚠️ ALERT: LOW MOISTURE' : '🔄 Status Normal'}
                        </span>
                    </div>
                    <div class="space-y-2 text-sm">
                        <div class="flex justify-between"><span class="text-gray-400">Soil Moisture:</span> <span class="font-semibold ${isAlert ? 'text-red-400' : 'text-emerald-400'}">${field.moisture}%</span></div>
                        <div class="flex justify-between"><span class="text-gray-400">Water Used Today:</span> <span class="text-blue-400 font-medium">${field.waterConsumption} L</span></div>
                        <div class="flex justify-between"><span class="text-gray-400">Temperature:</span> <span>${field.temp}°C</span></div>
                        <div class="flex justify-between"><span class="text-gray-400">Next Irrigation:</span> <span class="text-amber-400">${field.schedule}</span></div>
                        <div class="flex justify-between"><span class="text-gray-400">Crop Health:</span> <span class="${field.health === 'Critical' || field.health === 'Stressed' ? 'text-red-400' : 'text-emerald-400'}">${field.health}</span></div>
                    </div>
                `;
                grid.appendChild(card);
            });
        }

        function calculateAnalytics(fields) {
            // Total Water
            const total = fields.reduce((sum, f) => sum + f.waterConsumption, 0);
            document.getElementById("totalWater").innerText = `${total.toLocaleString()} L`;

            // Lowest Moisture
            const sorted = [...fields].sort((a, b) => a.moisture - b.moisture);
            document.getElementById("lowestMoistureField").innerText = sorted[0].id;
            document.getElementById("lowestMoistureValue").innerText = `Moisture levels at running ${sorted[0].moisture}%`;

            // Global Critical Alert Banner
            const criticalAlerts = fields.filter(f => f.moisture < 30);
            const banner = document.getElementById("global-alert-banner");
            if (criticalAlerts.length > 0) {
                banner.innerHTML = `<span class="bg-red-500/20 text-red-400 px-3 py-1.5 rounded-lg border border-red-500/30 text-xs md:text-sm font-semibold flex items-center gap-1.5 alert-pulse">⚠️ Critical: ${criticalAlerts.length} Fields Need Water Instantly</span>`;
            } else {
                banner.innerHTML = `<span class="bg-emerald-500/20 text-emerald-400 px-3 py-1.5 rounded-lg border border-emerald-500/30 text-xs md:text-sm font-semibold flex items-center gap-1.5">✓ Systems Balanced</span>`;
            }
        }

        function generateRecommendations(fields) {
            const tbody = document.getElementById("recommendationTable");
            tbody.innerHTML = "";
            
            const prioritized = [...fields].sort((a, b) => a.moisture - b.moisture);
            
            prioritized.forEach((field, index) => {
                const tr = document.createElement("tr");
