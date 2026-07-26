import express from 'express';
import {
    sendMessage,
    getChatHistory,
    clearChatHistory,
} from '../controllers/chatController.js';
import { protect } from '../middlewares/authMiddleware.js';

const router = express.Router();

// Route 1: Send a message to the AI assistant (Protected)
router.post('/', protect, sendMessage);

// Route 2: Get chat history for a dataset (Protected - supports /:datasetId or /)
router.get('/:datasetId', protect, getChatHistory);
router.get('/', protect, getChatHistory);

// Route 3: Clear chat history for a dataset (Protected - supports /:datasetId or /)
router.delete('/:datasetId', protect, clearChatHistory);
router.delete('/', protect, clearChatHistory);

export default router;
