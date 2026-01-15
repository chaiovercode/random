#!/usr/bin/env python3
"""
HTML Architecture Diagram to PDF Converter
==========================================

This script converts the HTML architecture diagram to a high-quality PDF.
Uses playwright for headless browser rendering with proper styling.

Requirements:
pip install playwright weasyprint
playwright install chromium

Usage:
python html_to_pdf.py
"""

import asyncio
from playwright.async_api import async_playwright
import os
from pathlib import Path

# Your HTML content (copy the full HTML from the artifact)
HTML_CONTENT = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Casino Analysis - Professional Charts</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        
        .header {
            text-align: center;
            margin-bottom: 50px;
            padding-bottom: 30px;
            border-bottom: 2px solid #f0f0f0;
        }
        
        .header h1 {
            font-size: 2.5em;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
            font-weight: 700;
        }
        
        .header p {
            font-size: 1.2em;
            color: #666;
            margin: 10px 0 0 0;
        }
        
        .chart-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            margin-bottom: 40px;
        }
        
        .chart-container {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            position: relative;
        }
        
        .chart-full {
            grid-column: 1 / -1;
        }
        
        .chart-title {
            font-size: 1.4em;
            font-weight: 600;
            margin-bottom: 20px;
            color: #333;
            text-align: center;
        }
        
        .chart-subtitle {
            font-size: 0.9em;
            color: #888;
            text-align: center;
            margin-bottom: 25px;
        }
        
        canvas {
            max-height: 400px !important;
        }
        
        .insights {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-top: 40px;
        }
        
        .insights h3 {
            margin-top: 0;
            font-size: 1.5em;
            margin-bottom: 20px;
        }
        
        .insight-item {
            margin-bottom: 15px;
            padding-left: 20px;
            position: relative;
        }
        
        .insight-item::before {
            content: '💡';
            position: absolute;
            left: 0;
            top: 0;
        }
        
        .key-metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
        }
        
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .metric-label {
            font-size: 0.9em;
            opacity: 0.9;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Casino Game Analysis</h1>
            <p>House Edge vs Player Engagement • Profit Load Analysis • Publisher Performance</p>
        </div>

        <div class="key-metrics">
            <div class="metric-card">
                <div class="metric-value">47</div>
                <div class="metric-label">Active Games (≥100 players)</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">41,334</div>
                <div class="metric-label">Total Active Players</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">1-3%</div>
                <div class="metric-label">Optimal House Edge</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">99%</div>
                <div class="metric-label">Top Game RTP</div>
            </div>
        </div>
        
        <div class="chart-grid">
            <div class="chart-container">
                <div class="chart-title">Players vs House Edge</div>
                <div class="chart-subtitle">Clear inverse relationship - higher edge = lower adoption</div>
                <canvas id="scatterChart"></canvas>
            </div>
            
            <div class="chart-container">
                <div class="chart-title">Publisher Impact</div>
                <div class="chart-subtitle">Weighted profit (Edge × Players) for active games</div>
                <canvas id="publisherChart"></canvas>
            </div>
        </div>
        
        <div class="chart-container chart-full">
            <div class="chart-title">Top 15 Games by Expected Profit Load</div>
            <div class="chart-subtitle">Games that combine decent margins with actual player volume</div>
            <canvas id="profitChart"></canvas>
        </div>
        
        <div class="insights">
            <h3>Key Strategic Insights</h3>
            <div class="insight-item">
                <strong>The 1% Edge Sweet Spot:</strong> Stake Originals with 1% house edge generate 250+ players per game vs 6.5 for 3-4% edge games
            </div>
            <div class="insight-item">
                <strong>Concentration Effect:</strong> Top 20 games drive 55-60% of expected profit load - a few hits carry the entire operation
            </div>
            <div class="insight-item">
                <strong>Publisher Trinity:</strong> Stake + Pragmatic + Evolution = 80% of weighted profit from active games
            </div>
            <div class="insight-item">
                <strong>Volume > Margin:</strong> Low-edge, high-volume strategy outperforms high-edge, low-volume by 10:1 ratio
            </div>
            <div class="insight-item">
                <strong>24-Tile Lobby Blueprint:</strong> 8-10 Originals + 6-8 Live + 6-8 proven slots beats 2000+ random games
            </div>
        </div>
    </div>

    <script>
        // Chart.js defaults for clean appearance
        Chart.defaults.plugins.legend.display = false;
        Chart.defaults.elements.point.backgroundColor = '#ff6b6b';
        Chart.defaults.elements.point.borderColor = '#ff6b6b';
        Chart.defaults.elements.point.borderWidth = 0;
        Chart.defaults.elements.point.radius = 6;
        Chart.defaults.elements.point.hoverRadius = 8;

        // Sample data based on the analysis (representative of actual patterns)
        const scatterData = [
            {x: 1, y: 3487}, {x: 1, y: 2587}, {x: 1, y: 2541}, {x: 1, y: 1899}, {x: 1, y: 1602},
            {x: 1, y: 1150}, {x: 0.6, y: 1134}, {x: 1, y: 927}, {x: 2, y: 734}, {x: 2.7, y: 610},
            {x: 1, y: 609}, {x: 3.74, y: 587}, {x: 3.5, y: 497}, {x: 2, y: 442}, {x: 6.01, y: 350},
            {x: 5.82, y: 349}, {x: 2, y: 288}, {x: 3.68, y: 254}, {x: 3.73, y: 245}, {x: 3.73, y: 211},
            {x: 3.5, y: 208}, {x: 3.86, y: 204}, {x: 3.45, y: 184}, {x: 3.62, y: 178}, {x: 3.41, y: 171},
            {x: 3.87, y: 157}, {x: 1.71, y: 150}, {x: 3.66, y: 149}, {x: 3.68, y: 148}, {x: 4.17, y: 147},
            {x: 3.95, y: 146}, {x: 3.76, y: 143}, {x: 3.93, y: 139}, {x: 3.89, y: 138}, {x: 3.44, y: 135},
            {x: 3.41, y: 134}, {x: 3.79, y: 133}, {x: 3.65, y: 132}, {x: 3.49, y: 131}, {x: 3.77, y: 129},
            {x: 3.78, y: 128}, {x: 3.64, y: 127}, {x: 3.47, y: 126}, {x: 3.69, y: 125}, {x: 3.81, y: 124},
            {x: 3.93, y: 123}, {x: 4.22, y: 121}
        ];

        // Publishers data (top performers)
        const publisherData = [
            {publisher: 'Stake', profit: 18170},
            {publisher: 'Pragmatic Play', profit: 4350},
            {publisher: 'Evolution', profit: 3890},
            {publisher: 'Hacksaw Gaming', profit: 2180},
            {publisher: 'Novomatic', profit: 1840},
            {publisher: 'Dragon', profit: 1470},
            {publisher: 'Nolimit City', profit: 940},
            {publisher: 'Pump', profit: 884}
        ];

        // Top games by profit score
        const topGames = [
            {name: 'Türkçe Futbol Stüdyosu', score: 4230},
            {name: 'mines', score: 3487},
            {name: 'dice', score: 2587},
            {name: 'limbo', score: 2541},
            {name: 'Le Zeus', score: 2194},
            {name: 'crash', score: 1899},
            {name: 'Gates of Olympus 1000', score: 1741},
            {name: 'Roulette Lobby', score: 1647},
            {name: 'plinko', score: 1602},
            {name: 'Dragon Tower', score: 1468},
            {name: 'Crazy Time', score: 1296},
            {name: 'keno', score: 1150},
            {name: 'Pump', score: 884},
            {name: 'hilo', score: 609},
            {name: 'Wanted Dead or a Wild', score: 523}
        ];

        // Scatter Chart - Players vs House Edge
        const scatterCtx = document.getElementById('scatterChart').getContext('2d');
        new Chart(scatterCtx, {
            type: 'scatter',
            data: {
                datasets: [{
                    data: scatterData,
                    backgroundColor: function(context) {
                        const value = context.parsed.x;
                        if (value <= 1) return '#ff6b6b';
                        if (value <= 2) return '#4ecdc4';
                        if (value <= 3) return '#45b7d1';
                        return '#f39c12';
                    },
                    pointRadius: 8,
                    pointHoverRadius: 10
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.parsed.y} players at ${context.parsed.x}% edge`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        title: { display: true, text: 'House Edge (%)' },
                        grid: { display: false },
                        border: { display: false }
                    },
                    y: {
                        title: { display: true, text: 'Concurrent Players' },
                        grid: { display: false },
                        border: { display: false }
                    }
                }
            }
        });

        // Publisher Impact Chart
        const pubCtx = document.getElementById('publisherChart').getContext('2d');
        new Chart(pubCtx, {
            type: 'doughnut',
            data: {
                labels: publisherData.map(p => p.publisher),
                datasets: [{
                    data: publisherData.map(p => p.profit),
                    backgroundColor: [
                        '#ff6b6b', '#4ecdc4', '#45b7d1', '#f39c12',
                        '#9b59b6', '#e74c3c', '#2ecc71', '#34495e'
                    ],
                    borderWidth: 0,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { 
                        display: true, 
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true,
                            font: { size: 12 }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const value = context.raw.toLocaleString();
                                return `${context.label}: ${value} weighted profit`;
                            }
                        }
                    }
                }
            }
        });

        // Top Games Profit Chart
        const profitCtx = document.getElementById('profitChart').getContext('2d');
        new Chart(profitCtx, {
            type: 'bar',
            data: {
                labels: topGames.map(g => g.name),
                datasets: [{
                    data: topGames.map(g => g.score),
                    backgroundColor: function(context) {
                        const colors = [
                            '#ff6b6b', '#4ecdc4', '#45b7d1', '#f39c12', '#9b59b6',
                            '#e74c3c', '#2ecc71', '#34495e', '#f1c40f', '#e67e22',
                            '#95a5a6', '#3498db', '#8e44ad', '#16a085', '#27ae60'
                        ];
                        return colors[context.dataIndex] || '#95a5a6';
                    },
                    borderRadius: 6,
                    borderSkipped: false
                }]
            },
            options: {
                responsive: true,
                indexAxis: 'y',
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Profit Score: ${context.raw.toLocaleString()}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        title: { display: true, text: 'Expected Profit Load (Edge × Players)' },
                        grid: { display: false },
                        border: { display: false }
                    },
                    y: {
                        grid: { display: false },
                        border: { display: false },
                        ticks: {
                            maxTicksLimit: 15
                        }
                    }
                }
            }
        });
    </script>
</body>
</html>
'''

async def create_pdf_with_playwright():
    """Create PDF using Playwright (recommended for complex layouts)"""
    
    # Create temp HTML file
    temp_html = Path("architecture_diagram.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Load the HTML file
        await page.goto(f"file://{temp_html.absolute()}")
        
        # Wait for content to load
        await page.wait_for_load_state('networkidle')
        
        # Generate PDF with high quality settings
        pdf_path = "AI_Customer_Service_Architecture.pdf"
        await page.pdf(
            path=pdf_path,
            format='A4',
            print_background=True,
            margin={
                'top': '0.5in',
                'bottom': '0.7in',
                'left': '0.5in',
                'right': '0.5in'
            },
            prefer_css_page_size=True,
            display_header_footer=True,
            header_template='<div></div>',  # Empty header
            footer_template='<div style="font-size:10px; margin:auto; color:#718096;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>'
        )
        
        await browser.close()
        
        # Clean up temp file
        temp_html.unlink()
        
        print(f"✅ PDF successfully created: {pdf_path}")
        return pdf_path

def create_pdf_with_weasyprint():
    """Alternative method using WeasyPrint"""
    try:
        from weasyprint import HTML, CSS
        from weasyprint.text.fonts import FontConfiguration
        
        # Additional CSS for print optimization
        print_css = CSS(string='''
            @page {
                size: A4;
                margin: 0.5in 0.5in 0.7in 0.5in;
                @bottom-center {
                    content: "Page " counter(page) " of " counter(pages);
                    font-size: 10px;
                    color: #718096;
                }
            }
            
            body { 
                background: white !important; 
                font-size: 12px;
            }
            
            .container {
                background: white !important;
                box-shadow: none !important;
            }
            
            .layer, .flow-step, .branch-container {
                break-inside: avoid;
            }
            
            .flow-diagram {
                background: #f7fafc !important;
            }
        ''')
        
        font_config = FontConfiguration()
        html = HTML(string=HTML_CONTENT)
        pdf_path = "AI_Customer_Service_Architecture_WeasyPrint.pdf"
        html.write_pdf(pdf_path, stylesheets=[print_css], font_config=font_config)
        
        print(f"✅ PDF successfully created with WeasyPrint: {pdf_path}")
        return pdf_path
        
    except ImportError:
        print("❌ WeasyPrint not installed. Install with: pip install weasyprint")
        return None

if __name__ == "__main__":
    print("🚀 Converting HTML Architecture Diagram to PDF...")
    print("="*50)
    
    # Method 1: Playwright (recommended)
    try:
        pdf_path = asyncio.run(create_pdf_with_playwright())
        print(f"📄 High-quality PDF created: {pdf_path}")
    except Exception as e:
        print(f"❌ Playwright method failed: {e}")
        print("💡 Trying WeasyPrint as fallback...")
        
        # Method 2: WeasyPrint fallback
        pdf_path = create_pdf_with_weasyprint()
        if pdf_path:
            print(f"📄 PDF created with WeasyPrint: {pdf_path}")
        else:
            print("❌ Both methods failed. Please install required packages:")
            print("   pip install playwright weasyprint")
            print("   playwright install chromium")