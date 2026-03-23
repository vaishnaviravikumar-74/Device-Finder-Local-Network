import subprocess
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def handler(request):
    """
    Vercel serverless function handler.
    For Streamlit apps, we return a message indicating the app is running.
    The actual Streamlit app runs as a separate process.
    """
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/html'},
        'body': '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Device Finder - Local Network</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {
                    font-family: system-ui, -apple-system, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                }
                .container {
                    text-align: center;
                    background: white;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
                }
                h1 { color: #333; margin: 0 0 10px 0; }
                p { color: #666; margin: 10px 0; }
                .spinner {
                    border: 4px solid #f3f3f3;
                    border-top: 4px solid #667eea;
                    border-radius: 50%;
                    width: 40px;
                    height: 40px;
                    animation: spin 1s linear infinite;
                    margin: 20px auto;
                }
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔍 Device Finder - Local Network</h1>
                <div class="spinner"></div>
                <p>Loading Streamlit application...</p>
                <p>If the app doesn't load in a few seconds, please refresh the page.</p>
            </div>
            <script>
                setTimeout(function() {
                    window.location.reload();
                }, 3000);
            </script>
        </body>
        </html>
        '''
    }
