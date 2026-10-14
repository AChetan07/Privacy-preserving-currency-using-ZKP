// Transaction timing data - sample values that work without Flask
const timingData = {
    btc: 10500,    // Bitcoin
    xmr: 5500,     // Monero  
    zec: 2000,     // Zcash
    our: 0.057     // Our ZKP System
};

document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('timingChartContainer');
    if (!container) return;
    
    // Find the maximum value for scaling (use Bitcoin as reference)
    const maxValue = Math.max(timingData.btc, 1);
    
    // Create bar chart HTML
    const coins = [
        { name: 'Bitcoin', value: timingData.btc, color: 'linear-gradient(135deg, #f7931a, #d98416)', textColor: '#f7931a' },
        { name: 'Monero', value: timingData.xmr, color: 'linear-gradient(135deg, #5eead4, #3db8a8)', textColor: '#5eead4' },
        { name: 'Zcash', value: timingData.zec, color: 'linear-gradient(135deg, #d4a574, #b8956a)', textColor: '#d4a574' },
        { name: 'Our ZKP', value: timingData.our, color: 'linear-gradient(135deg, #8b7ec8, #6b5fa0)', textColor: '#8b7ec8' }
    ];
    
    coins.forEach(coin => {
        const barWidth = Math.max((coin.value / maxValue) * 100, 2);
        
        const row = document.createElement('div');
        row.className = 'chart-bar-row';
        
        row.innerHTML = `
            <div class="chart-bar-label">${coin.name}</div>
            <div class="chart-bar-container">
                <div class="chart-bar-fill" style="width: ${barWidth}%; background: ${coin.color};">
                    ${coin.value.toFixed(3)} ms
                </div>
            </div>
            <div class="chart-bar-value" style="color: ${coin.textColor};">
                ${coin.value.toFixed(3)} ms
            </div>
        `;
        
        container.appendChild(row);
    });
});