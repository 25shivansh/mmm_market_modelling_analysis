import express from 'express';
import {
    getAllReports,
    getReportById,
    downloadReport,
    deleteReport,
} from '../controllers/reportController.js';
import { protect } from '../middlewares/authMiddleware.js';

const router = express.Router();

// Route 1: Get all reports for logged-in user (Protected)
router.get('/', protect, getAllReports);

// Route 2: Get a single report by ID (Protected)
router.get('/:id', protect, getReportById);

// Route 3: Download report data by ID (Protected)
router.get('/:id/download', protect, downloadReport);

// Route 4: Delete a report by ID (Protected)
router.delete('/:id', protect, deleteReport);

export default router;
