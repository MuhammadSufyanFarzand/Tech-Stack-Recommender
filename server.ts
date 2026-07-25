import express from 'express';
import path from 'path';
import fs from 'fs';
import { exec, execSync } from 'child_process';
import { createServer as createViteServer } from 'vite';

const app = express();
const PORT = 3000;

app.use(express.json({ limit: '10mb' }));

const PROJECT_DIR = path.join(process.cwd(), 'tech-stack-recommender');
const ZIP_FILE_PATH = path.join(PROJECT_DIR, 'tech-stack-recommender.zip');

// Ensure project directory exists
if (!fs.existsSync(PROJECT_DIR)) {
  fs.mkdirSync(PROJECT_DIR, { recursive: true });
}

// -------------------------------------------------------------
// API ROUTES
// -------------------------------------------------------------

// 1. Health check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    project: 'Tech Stack Recommender',
    algorithm: 'TF-IDF Vectorization & Cosine Similarity',
    python_version: '3.10+'
  });
});

// 2. Recommend Tech Stacks via Python Service
app.post('/api/recommend', (req, res) => {
  const query = req.body?.query || '';
  const top_n = req.body?.top_n || 5;

  if (!query.trim()) {
    return res.status(400).json({ error: 'Please provide a non-empty query string.' });
  }

  // Escape query safely for python command argument
  const pyCode = `
import sys, json, os
sys.path.insert(0, '${PROJECT_DIR.replace(/\\/g, '/')}')
from app import TechStackRecommenderService

data_path = os.path.join('${PROJECT_DIR.replace(/\\/g, '/')}', 'data', 'raw_skills.csv')
model_dir = os.path.join('${PROJECT_DIR.replace(/\\/g, '/')}', 'models')

svc = TechStackRecommenderService(data_path, model_dir)
svc.initialize()

result = svc.recommend_for_query("""${query.replace(/"""/g, '')}""", top_n=${top_n})
print(json.dumps(result))
`;

  exec(`python3 -c "${pyCode.replace(/"/g, '\\"')}"`, { cwd: process.cwd() }, (error, stdout, stderr) => {
    if (error) {
      console.error('Python execution error:', stderr || error.message);
      return res.status(500).json({
        error: 'Failed to run TF-IDF Recommender engine.',
        details: stderr || error.message
      });
    }

    try {
      // Parse last line of stdout which contains JSON
      const lines = stdout.trim().split('\n');
      const jsonLine = lines[lines.length - 1];
      const parsedData = JSON.parse(jsonLine);
      return res.json({ status: 'success', data: parsedData });
    } catch (parseErr) {
      console.error('JSON parse error from python output:', stdout);
      return res.status(500).json({
        error: 'Failed to parse recommendation output.',
        raw: stdout
      });
    }
  });
});

// 3. Get Project Files for Code Viewer
app.get('/api/files', (req, res) => {
  const fileTree: Array<{ path: string; relativePath: string; type: 'file' | 'dir'; size?: number; content?: string }> = [];

  function scanDir(dirPath: string) {
    if (!fs.existsSync(dirPath)) return;
    const items = fs.readdirSync(dirPath, { withFileTypes: true });

    for (const item of items) {
      if (item.name === '__pycache__' || item.name === 'node_modules' || item.name.endsWith('.zip') || item.name === '.git') {
        continue;
      }

      const fullPath = path.join(dirPath, item.name);
      const relPath = path.relative(PROJECT_DIR, fullPath);

      if (item.isDirectory()) {
        fileTree.push({ path: fullPath, relativePath: relPath, type: 'dir' });
        scanDir(fullPath);
      } else if (item.isFile()) {
        let content = '';
        try {
          if (!item.name.endsWith('.pkl') && !item.name.endsWith('.zip')) {
            content = fs.readFileSync(fullPath, 'utf-8');
          }
        } catch (e) {
          content = '(Binary file)';
        }

        const stat = fs.statSync(fullPath);
        fileTree.push({
          path: fullPath,
          relativePath: relPath,
          type: 'file',
          size: stat.size,
          content
        });
      }
    }
  }

  scanDir(PROJECT_DIR);
  return res.json({ status: 'success', files: fileTree });
});

// 4. Save Edits to Project Files
app.post('/api/files/save', (req, res) => {
  const { relativePath, content } = req.body;
  if (!relativePath || content === undefined) {
    return res.status(400).json({ error: 'Missing relativePath or content' });
  }

  const targetPath = path.join(PROJECT_DIR, relativePath);
  try {
    fs.mkdirSync(path.dirname(targetPath), { recursive: true });
    fs.writeFileSync(targetPath, content, 'utf-8');
    return res.json({ status: 'success', message: `Saved ${relativePath}` });
  } catch (err: any) {
    return res.status(500).json({ error: err.message });
  }
});

// 5. Trigger create_zip.py and Download Zip
app.get('/api/download-zip', (req, res) => {
  try {
    const pyScript = path.join(PROJECT_DIR, 'create_zip.py');
    execSync(`python3 "${pyScript}"`, { cwd: PROJECT_DIR });

    if (fs.existsSync(ZIP_FILE_PATH)) {
      res.setHeader('Content-Type', 'application/zip');
      res.setHeader('Content-Disposition', 'attachment; filename="tech-stack-recommender.zip"');
      return res.sendFile(ZIP_FILE_PATH);
    } else {
      return res.status(500).json({ error: 'ZIP file creation failed.' });
    }
  } catch (err: any) {
    return res.status(500).json({ error: 'Failed to create zip file.', details: err.message });
  }
});

// -------------------------------------------------------------
// VITE / STATIC SERVING
// -------------------------------------------------------------
async function startServer() {
  if (process.env.NODE_ENV !== 'production') {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: 'spa'
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), 'dist');
    app.use(express.static(distPath));
    app.get('*', (req, res) => {
      res.sendFile(path.join(distPath, 'index.html'));
    });
  }

  app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server listening at http://0.0.0.0:${PORT}`);
  });
}

startServer();
