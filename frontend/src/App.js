import './App.css';
import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';

function App() {
  const [stats, setStats] = useState({ total_scanned: 0, genuine: 0, counterfeit: 0, yield_rate: 0 });
  const [file, setFile] = useState(null);
  const [partNumber, setPartNumber] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const API_BASE = 'http://localhost:8000';

  const fetchStats = useCallback(async () => {
    try {
      const response = await axios.get(`${API_BASE}/api/v1/stats`);
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  }, [API_BASE]);

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 2000); // Updates every 2 seconds
    return () => clearInterval(interval);
  }, [fetchStats]);

  const handleScan = async (e) => {
    e.preventDefault();
    if (!file || !partNumber) {
      alert('Please select a file and enter part number');
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('part_number', partNumber);

      const response = await axios.post(`${API_BASE}/api/v1/scan-ic`, formData);
      
      // Use actual response from backend
      const verdict = response.data.status.includes('PASS') ? 'GENUINE' : 'COUNTERFEIT';
      const issues = response.data.issues || [];
      
      setResult({
        file_id: response.data.file_id,
        part_number: response.data.part_number,
        verdict: verdict,
        confidence: response.data.confidence.toFixed(2),
        issues: issues,
        explanation: response.data.explanation || '',
        detected_data: response.data.detected_data || {},
        timestamp: new Date().toLocaleString()
      });

      setFile(null);
      setPartNumber('');
      
      // Refresh stats immediately - multiple times for instant visual feedback
      await fetchStats();
      setTimeout(() => fetchStats(), 300);
      setTimeout(() => fetchStats(), 600);
      setTimeout(() => fetchStats(), 1000);
    } catch (error) {
      console.error('Scan error:', error);
      alert('Error submitting scan');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="navbar">
        <div className="navbar-content">
          <h1>🛡️ MarkGuard AI</h1>
          <p>AI-Powered Real-Time IC Authentication</p>
        </div>
      </header>

      <main className="container">
        {/* Stats Section */}
        <section className="stats-section">
          <div className="stat-box">
            <div className="stat-number">{stats.total_scanned.toLocaleString()}</div>
            <div className="stat-label">Total Scanned</div>
          </div>
          <div className="stat-box genuine">
            <div className="stat-number">{stats.genuine.toLocaleString()}</div>
            <div className="stat-label">Genuine ICs</div>
          </div>
          <div className="stat-box counterfeit">
            <div className="stat-number">{stats.counterfeit}</div>
            <div className="stat-label">Counterfeit Found</div>
          </div>
          <div className="stat-box yield">
            <div className="stat-number">{stats.yield_rate}%</div>
            <div className="stat-label">Yield Rate</div>
          </div>
        </section>

        {/* Main Content */}
        <div className="main-grid">
          {/* Upload Section */}
          <section className="upload-section card">
            <h2>📸 Scan IC</h2>
            <form onSubmit={handleScan}>
              <div className="form-group">
                <label>Upload Image:</label>
                <div className="file-input">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={(e) => setFile(e.target.files[0])}
                    id="file-upload"
                  />
                  <label htmlFor="file-upload" className="file-label">
                    {file ? file.name : 'Choose Image'}
                  </label>
                </div>
              </div>
              <div className="form-group">
                <label>Part Number:</label>
                <input
                  type="text"
                  value={partNumber}
                  onChange={(e) => setPartNumber(e.target.value)}
                  placeholder="e.g., NE555DR"
                  required
                />
              </div>
              <button type="submit" disabled={loading} className="scan-btn">
                {loading ? '⏳ Scanning...' : '🔍 Scan IC'}
              </button>
            </form>
          </section>

          {/* Result Section */}
          {result && (
            <section className="result-section card">
              <h2>📋 Scan Result</h2>
              <div className={`verdict ${result.verdict.toLowerCase()}`}>
                <div className="verdict-text">
                  {result.verdict === 'GENUINE' ? '✅' : '❌'} {result.verdict}
                </div>
                <div className="confidence">Confidence: {result.confidence}%</div>
              </div>
              
              {/* AI Explanation */}
              <div className="explanation-box">
                <h3>🤖 AI Analysis</h3>
                <p>{result.explanation}</p>
              </div>

              <div className="result-details">
                <p><strong>Part Number:</strong> {result.part_number}</p>
                <p><strong>Scan ID:</strong> {result.file_id.substring(0, 8)}...</p>
                <p><strong>Time:</strong> {result.timestamp}</p>
                
                {/* Detected Data */}
                {result.detected_data && (
                  <div className="detected-info">
                    <strong>Detection Details:</strong>
                    <ul style={{listStyle: 'none', padding: '0.8rem 0'}}>
                      <li>📍 Manufacturer: <strong>{result.detected_data.manufacturer || 'Unknown'}</strong></li>
                      <li>🏷️ Expected Logo: <strong>{result.detected_data.expected_logo || 'N/A'}</strong></li>
                      <li>📊 Image Quality: <strong>{result.detected_data.image_quality || 'Unknown'}</strong></li>
                      <li>🔤 Detected Text: <strong>{result.detected_data.detected_texts && Array.isArray(result.detected_data.detected_texts) ? result.detected_data.detected_texts.join(', ') : 'None'}</strong></li>
                    </ul>
                  </div>
                )}
                
                {result.issues.length > 0 && (
                  <div className="issues">
                    <strong>⚠️ Issues Found:</strong>
                    <ul>
                      {result.issues.map((issue, i) => (
                        <li key={i}>{issue}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </section>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
