import express from 'express';
import database from '../config/database.js';

const router = express.Router();

router.get('/', async (req, res) => {
  try {
    // Check database connection
    const dbStatus = database.isReady() ? 'connected' : 'disconnected';
    let dbInfo = { status: dbStatus };
    
    if (database.isReady()) {
      try {
        const db = database.getDb();
        await db.admin().ping();
        dbInfo.ping = 'success';
      } catch (error) {
        dbInfo.ping = 'failed';
        dbInfo.error = error.message;
      }
    }
    
    res.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      memory: process.memoryUsage(),
      version: process.version,
      database: dbInfo,
    });
  } catch (error) {
    res.status(500).json({
      status: 'unhealthy',
      timestamp: new Date().toISOString(),
      error: error.message,
    });
  }
});

export default router;